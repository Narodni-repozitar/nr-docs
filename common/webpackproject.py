from flask_webpackext import (
    WebpackBundle,
    WebpackBundleProject as InvenioWebpackBundleProject,
)
from pywebpack import bundles_from_entry_point
from pywebpack.project import WebpackTemplateProject
from pynpm import NPMPackage as InvenioNPMPackage, YarnPackage
from pynpm.utils import run_npm
from os.path import basename, dirname, join
import shutil
import os
import json

two_folders_up = os.path.abspath(os.path.join(os.getcwd(), "..", ".."))


def package_files_exist():
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


def get_package_and_package_lock_files(project_path):
    """
    Navigate two directories up from the current working directory,
    check if `package.json` and `package-lock.json` exist,
    copy them to the specified project_path, and return True if successful.

    :param project_path: Path to the project directory where files should be copied.
    :return: True if both files exist and are copied, False otherwise.
    """
    # Navigate two folders up

    # Paths to package.json and package-lock.json
    package_json_path = os.path.join(two_folders_up, "package.json")
    package_lock_json_path = os.path.join(two_folders_up, "package-lock.json")

    # Check if both files exist
    if os.path.isfile(package_json_path) and os.path.isfile(package_lock_json_path):
        # Ensure the target directory exists
        os.makedirs(project_path, exist_ok=True)

        # Copy files to the target directory
        shutil.copy(package_json_path, project_path)
        shutil.copy(package_lock_json_path, project_path)

        return True
    else:
        return False


class NPMPackage(InvenioNPMPackage):
    def _run_npm(self, command, *args, **kwargs):
        """Run an NPM command.

        By default the call is blocking until NPM is finished and output
        is directed to stdout. If ``wait=False`` is passed to the method,
        you get a handle to the process (return value of ``subprocess.Popen``).

        :param command: NPM command to run.
        :param args: List of arguments.
        :param wait: Wait for NPM command to finish. By defaul
        """
        source_package_files = package_files_exist()
        package_files_same = False

        if command == "install":
            venv_package_json = self.package_json
            if source_package_files["exists"]:
                with open(source_package_files["package_json_path"], "r") as fp:
                    package_json_source = json.load(fp)
                    if venv_package_json == package_json_source:
                        package_files_same = True
                        shutil.copy(
                            source_package_files["package_lock_json_path"],
                            self._package_json_path,
                        )
            npm_install_return_code = run_npm(
                dirname(self.package_json_path),
                command,
                npm_bin=self._npm_bin,
                args=args,
                shell=self._shell,
                **kwargs,
            )

            if not package_files_same and npm_install_return_code == 0:
                print(
                    self._package_json_path,
                    "package_json_pathaaa",
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
        else:
            return run_npm(
                dirname(self.package_json_path),
                command,
                npm_bin=self._npm_bin,
                args=args,
                shell=self._shell,
                **kwargs,
            )

    # def copy_package_and_package_lock_to_sources(self);
    #     pass


# Example usage
# project_dir = "/path/to/project"
# result = get_package_and_package_lock_files(project_dir)
# print("Files copied successfully:" if result else "Files not found.")


class WebpackBundleProject(InvenioWebpackBundleProject):
    @property
    def npmpkg(self):
        """Get API to NPM package."""
        return NPMPackage(self.path)

    # def create(self, force=None):
    #     """Create webpack project from a template.

    #     This command collects all asset files from the bundles.
    #     It generates a new package.json by merging the package.json
    #     dependencies of each bundle.
    #     """
    #     # Skip package.json (because we will always write a new).
    #     WebpackTemplateProject.create(self, force=force, skip=["package.json"])
    #     # Collect all asset files from the bundles.
    #     self.collect(force=force)
    #     # Generate new package json (reads the package.json source and merges
    #     # in npm dependencies).
    # package_json = self.package_json
    # package_files = package_files_exist()
    # print(package_files, "package_files", flush=True)
    # if package_files["exists"]:
    #     with open(package_files["package_json_path"], "r") as fp:
    #         package_json_source = json.load(fp)
    #         if package_json == package_json_source:
    #             print(package_json == package_json_source, "equality", flush=True)
    #             shutil.copy(package_files["package_lock_json_path"], self.path)
    #     # Write package.json (with collected dependencies)
    #     with open(self.npmpkg.package_json_path, "w") as fp:
    #         json.dump(package_json, fp, indent=2, sort_keys=True)


project = WebpackBundleProject(
    "invenio_assets.webpack",
    project_folder="assets",
    config_path="build/config.json",
    bundles=bundles_from_entry_point("invenio_assets.webpack"),
)
