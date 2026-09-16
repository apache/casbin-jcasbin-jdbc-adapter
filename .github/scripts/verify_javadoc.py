# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

"""Check actual Javadoc assets and complete, self-contained license texts."""

from pathlib import Path
import sys
import zipfile

UPL_ASSETS = {
    "resource-files/copy.svg", "resource-files/external-link.svg",
    "resource-files/glass.svg", "resource-files/left.svg",
    "resource-files/link.svg", "resource-files/right.svg",
    "resource-files/stylesheet.css", "resource-files/x.svg",
    "script-files/script.js", "script-files/search-page.js",
    "script-files/search.js",
}
MIT_ASSETS = {
    "script-files/jquery-3.7.1.min.js": b"jQuery v3.7.1",
    "script-files/jquery-ui.min.js": b"jQuery UI - v1.14.1",
    "resource-files/jquery-ui.min.css": b"jQuery UI - v1.14.1",
}
INDEXES = {kind + "-search-index.js" for kind in
           ("member", "module", "package", "tag", "type")}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify(path, root):
    license_text = (root / "src/javadoc-legal/LICENSE").read_bytes()
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        require(len(names) == len(archive.namelist()), "Duplicate Javadoc entries")
        for name in ("META-INF/LICENSE", "legal/LICENSE"):
            require(archive.read(name) == license_text, "Incomplete license: " + name)
        for name in ("NOTICE", "DISCLAIMER"):
            require(archive.read("META-INF/" + name) == (root / name).read_bytes(),
                    "Incorrect project legal file: " + name)
        for name, version in MIT_ASSETS.items():
            require(name in names, "Missing expected asset: " + name)
            require(version in archive.read(name)[:300], "Unreviewed asset version: " + name)
        require("script-files/script.js" in names, "Expected JDK 25 documentation")
        for name in names:
            if name.endswith("/"):
                continue
            data = archive.read(name)
            if name.startswith(("resource-files/", "script-files/")):
                require(name in UPL_ASSETS or name in MIT_ASSETS,
                        "Unreviewed documentation resource: " + name)
                if name in UPL_ASSETS:
                    require(b"Universal Permissive License v 1.0" in data[:700],
                            "Missing resource license header: " + name)
            elif name.endswith((".js", ".css", ".svg", ".png", ".woff", ".woff2")):
                require(name in INDEXES, "Unreviewed documentation asset: " + name)
            if name.startswith("legal/"):
                require(name == "legal/LICENSE", "Unexpected legal file: " + name)
                require(not data.lstrip().startswith(b"Please see"), "Dangling license pointer")
        page = archive.read("index.html").decode("utf-8")
        require("javadoc (25" in page, "Unreviewed Javadoc generator")
        require("Incubation is required of all newly accepted projects" in page,
                "Missing visible incubation disclaimer")
    print("Verified Javadoc resources and licenses: " + str(path))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: verify_javadoc.py path/to/javadoc.jar")
    verify(Path(sys.argv[1]), Path(__file__).resolve().parents[2])
