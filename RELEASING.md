<!--
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements. See the NOTICE file
distributed with this work for additional information
regarding copyright ownership. The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License. You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied. See the License for the
specific language governing permissions and limitations
under the License.
-->

# Releasing JDBC Adapter for JCasbin

Complete version, dependency, licensing, packaging and build/test preparation
in one PR. After merge, freeze the actual commit, check its CI and verify its
source archive. Review LICENSE, NOTICE, DISCLAIMER and every RAT exclusion.
Run `python3 -m unittest discover -s .github/scripts -p 'test_*.py'` for the
publication checks (Python 3.11+). A green build does not replace release votes.

## RC and votes

At the reviewed commit, create `vX.Y.Z-rcN` with the plain `X.Y.Z` already in
pom.xml. The workflow creates a GitHub prerelease containing
`apache-casbin-jdbc-adapter-X.Y.Z-incubating-src.tar.gz` and its `.sha512`.
RC jobs do not load registry/signing credentials or publish registry packages.

Download, inspect and independently build the exact generated archive. Sign
it to produce `.asc`, then stage all three files in
`https://dist.apache.org/repos/dist/dev/incubator/casbin/jdbc-adapter-X.Y.Z-incubating-rcN/`.
Confirm the signer is in the official Casbin KEYS file and that the publisher
has ASF distribution write access. Verify public downloads, checksum and
signature before conducting the applicable project and Incubator votes.
Never overwrite a staged candidate: changed bytes require a new RC number.

## Final release

After the applicable votes pass, promote the same three files to the ASF
release directory `incubator/casbin/jdbc-adapter-X.Y.Z-incubating/`. Wait until
all files are available under `https://downloads.apache.org/incubator/casbin/`.
Create `vX.Y.Z` at the reviewed RC commit. The final workflow downloads these
originals, verifies SHA-512 and GPG against Casbin KEYS, and compares their file
contents with Git. It does not rebuild or replace the voted source archive.

GitHub Release creation refuses an existing Release. Registry publication
runs only after the GitHub Release succeeds, and independently verifies ASF
originals before loading publication credentials. On a registry job failure,
check the registry version first, then use GitHub Actions to rerun only failed
jobs if publication did not complete. Do not delete/recreate voted candidates
or rerun all jobs to replace existing assets. Keep vote results, artifact
checks and publication evidence together; send announcements as authorized.

Maven publication uses `GPG_PRIVATE_KEY`, `GPG_PASSPHRASE`,
`OSSRH_JIRA_USERNAME` and `OSSRH_JIRA_PASSWORD`. The legacy OSSRH-named
values must be Central Publisher Portal user-token credentials authorized
for `org.casbin`, not obsolete OSSRH account credentials.

## Build from an extraction

Use Java 8 and Maven 3.9.x with MySQL, PostgreSQL and SQL Server available.
Run `mvn -B -ntp clean verify -Dgpg.skip=true`; the CI also runs
`cobertura:cobertura`. Do not use `deploy` during verification.

Tests default to local ports 3306, 5432 and 1433 with the disposable test
credentials in `AdapterCreator.java`. Set `JDBC_TEST_MYSQL_URL`,
`JDBC_TEST_POSTGRES_URL` and `JDBC_TEST_SQLSERVER_URL` for isolated ports.
Use dedicated empty databases; never point these tests at production data.
For MySQL, retain the default connection URL options when changing its port.
Test fixtures may change, so use a disposable source extraction. The default
build does not require an Oracle driver; Oracle applications configure their
own driver as described in README.md. Oracle is not part of the automated
test suite.


## Distribution review

This preparation preserves the existing `org.casbin:jdbc-adapter` coordinates and the
selected package version for consumer compatibility; the ASF source archive
name includes `incubating`. Before an RC, record the project's disposition of
the Incubator distribution naming guidance and any required exception. This
compatibility choice is not evidence of IPMC approval or registry ownership.

Review the incubation disclaimer in the README, package metadata where
applicable, and generated GitHub notes. Before publication, verify the ASF
download/verification links and that project maintainers can administer each
registry. Track Git tag, ASF dev/release, signing/KEYS, and registry permissions
separately. Keep actual decisions and provenance evidence with the release
record, outside the source distribution; header text is not proof of a grant.
