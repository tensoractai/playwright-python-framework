import os
import pytest
import allure
from playwright.sync_api import sync_playwright

from run_tests import (
    HEADLESS,
    SLOW_MO,
    VIEWPORT,
    DEFAULT_TIMEOUT,
    NAVIGATION_TIMEOUT,
    VIDEO,
)

import subprocess

def trim_video_last_20_seconds(input_path, output_path):
    try:
        import imageio_ffmpeg
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        cmd = [
            ffmpeg_exe,
            "-y",
            "-sseof", "-20",
            "-i", input_path,
            "-c", "copy",
            output_path
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            return output_path
    except Exception as e:
        print(f"Video trimming notice: {e}")
    return input_path

@pytest.fixture
def page(request):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=HEADLESS,
            slow_mo=SLOW_MO
        )

        test_path = str(request.node.fspath)
        test_folder = os.path.basename(os.path.dirname(test_path))
        test_file = os.path.splitext(os.path.basename(test_path))[0]
        test_func = request.node.name

        if test_folder:
            video_dir = os.path.join("videos", test_folder)
        else:
            video_dir = "videos"

        context_kwargs = {
            "viewport": VIEWPORT,
            "ignore_https_errors": True,
        }

        if VIDEO:
            os.makedirs(video_dir, exist_ok=True)
            context_kwargs["record_video_dir"] = video_dir

        context = browser.new_context(**context_kwargs)
        context.set_default_timeout(DEFAULT_TIMEOUT)
        context.set_default_navigation_timeout(NAVIGATION_TIMEOUT)
        page = context.new_page()

        yield page

        video_object = page.video
        context.close()

        # Check if test failed or encountered an error
        rep_call = getattr(request.node, "rep_call", None)
        rep_setup = getattr(request.node, "rep_setup", None)
        is_failed = (rep_call and rep_call.failed) or (rep_setup and rep_setup.failed)

        if VIDEO and video_object:
            try:
                raw_video_path = video_object.path()
                if raw_video_path and os.path.exists(raw_video_path):
                    clean_file = "".join(c for c in test_file if c.isalnum() or c in ("_", "-"))
                    clean_func = "".join(c for c in test_func if c.isalnum() or c in ("_", "-"))

                    if clean_file and clean_func and clean_file.lower() != clean_func.lower():
                        base_name = f"{clean_file}_{clean_func}"
                    else:
                        base_name = clean_file or clean_func or "test_video"

                    new_video_path = os.path.join(os.path.dirname(raw_video_path), f"{base_name}.webm")

                    if os.path.exists(new_video_path) and new_video_path != raw_video_path:
                        try:
                            os.remove(new_video_path)
                        except Exception:
                            pass

                    os.rename(raw_video_path, new_video_path)
                    raw_video_path = new_video_path

                    if is_failed:
                        trimmed_path = os.path.join(
                            os.path.dirname(raw_video_path),
                            f"{base_name}_last_20s.webm"
                        )
                        final_path = trim_video_last_20_seconds(raw_video_path, trimmed_path)
                        allure.attach.file(
                            final_path,
                            name=f"Failure Video ({base_name})",
                            attachment_type=allure.attachment_type.WEBM
                        )
            except Exception as e:
                print(f"Failed to process video file: {e}")

        browser.close()


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    folder_name = os.path.basename(os.path.dirname(str(item.fspath)))
    file_name = os.path.splitext(os.path.basename(str(item.fspath)))[0]

    allure.dynamic.parent_suite(folder_name)
    allure.dynamic.suite(file_name)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    test_path = os.path.normpath(str(item.fspath))
    # Get testcase folder name: datasets / files
    pytest.current_test_folder = os.path.basename(
        os.path.dirname(test_path)
    )
    # Get testcase file name without .py
    pytest.current_test_file = os.path.splitext(
        os.path.basename(test_path)
    )[0]
    yield
    pytest.current_test_folder = None
    pytest.current_test_file = None

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
