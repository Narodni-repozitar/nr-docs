from flask_webpackext import (
    WebpackBundleProject as InvenioWebpackBundleProject,
)
from pywebpack import bundles_from_entry_point
from pynpm import NPMPackage as InvenioNPMPackage
from pynpm.utils import run_npm
from os.path import dirname, join
import shutil
import os
import json

# not sure how to reference the top level folder of a project in the section
# that deals with webpack related commands (here referred to "invenio webpack"commands)
two_folders_up = os.path.abspath(os.path.join(os.getcwd(), "..", ".."))


def source_package_files_exist():
    package_json_path = os.path.join(two_folders_up, "package.json")
    package_lock_json_path = os.path.join(two_folders_up, "package-lock.json")
    if os.path.isfile(package_json_path) and os.path.isfile(package_lock_json_path):
        return {
            "exists": True,
            "package_json_path": package_json_path,
            "package_lock_json_path": package_lock_json_path,
        }
    else:
        return {
            "exists": False,
            "package_json_path": package_json_path,
            "package_lock_json_path": package_lock_json_path,
        }


class NPMPackage(InvenioNPMPackage):
    def install(self, *args, **kwargs):
        """Handle the NPM install command with additional logic."""
        source_package_files = source_package_files_exist()
        package_files_same = False

        venv_package_json = self.package_json
        if source_package_files["exists"]:
            with open(source_package_files["package_json_path"], "r") as fp:
                package_json_source = json.load(fp)
                if venv_package_json == package_json_source:
                    package_files_same = True
                    print("Copying package lock to venv", flush=True)
                    shutil.copy(
                        source_package_files["package_lock_json_path"],
                        self._package_json_path,
                    )
                else:
                    print("Package files are different", flush=True)

        npm_install_return_code = run_npm(
            dirname(self.package_json_path),
            "install",
            npm_bin=self._npm_bin,
            args=args,
            shell=self._shell,
            **kwargs,
        )

        if not package_files_same and npm_install_return_code == 0:
            print(
                "Copying package.json and package-lock.json to source directory",
                flush=True,
            )
            shutil.copy(
                join(self._package_json_path, "package.json"),
                source_package_files["package_json_path"],
            )
            shutil.copy(
                join(self._package_json_path, "package-lock.json"),
                source_package_files["package_lock_json_path"],
            )

        return npm_install_return_code


class WebpackBundleProject(InvenioWebpackBundleProject):
    @property
    def npmpkg(self):
        """Get API to NPM package."""
        return NPMPackage(self.path)


project = WebpackBundleProject(
    "invenio_assets.webpack",
    project_folder="assets",
    config_path="build/config.json",
    bundles=bundles_from_entry_point("invenio_assets.webpack"),
)
