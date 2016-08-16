# Katello Packaging

## Requirements

If you're just submitting a fix, you don't need anything special.

If you're just submitting a patch which changes a source file, you will need:

* [git-annex](http://git-annex.branchable.com/)
* [gem-compare](https://rubygems.org/gems/gem-compare)

However to release RPMs from this repo, you also require:

* koji client and an account (certificate) on koji.katello.org
* [tito](https://github.com/dgoodwin/tito) 0.5.6 or higher
* ``scl-utils-build`` for scl packages
* [quvi](http://koji.fedoraproject.org/koji/packageinfo?packageID=10165) package that is used by git-annex

## HOWTO: checkout

Run:

* `git clone https://github.com/katello/katello-packaging`
* `git annex init` to set up this repo for using git annex
* `./setup_sources.sh` to register git-annex file URLs

## HOWTO: test a package

Before tagging a build, please test it.  Using tito's --test flag, you can
generate test (S)RPMs by first committing your changes locally, then it will
use the SHA in the RPM version.

### With mock

Configuration for mock is supplied in mock/ and can be used to build any of
the packages locally and quickly.

1. Copy mock/site-defaults.cfg.basic to site-defaults.cfg, or look at other
   example configs for more options.
1. `tito build --rpm --test --builder builder.MockBuilder --arg mock_config_dir=mock/ --arg mock=el6-scl`

The last argument is the name of the mock config in mock/, which includes SCL
and non-SCL variants.

### With koji access

If you have a certificate for our Koji server (regular packagers can get them),
then you can use tito to build scratch packages on Koji, though it's slower
than mock (above).

With sources in git(-annex):

    tito release koji-katello --test --scratch

### Alternative method with koji access

lzap's [sbu utility](https://github.com/lzap/bin-public/blob/master/sbu) is
good for building test packages, especially with sources from elsewhere:

1. sbu (defaults for EL6 with SCL)
1. sbu katello fc19 katello-nightly-fedora19
1. sbu katello el6 katello-nightly-nonscl-rhel6

Most packages should build for EL6 and EL7 with SCL.

To be able to build katello core packages with sbu, one needs to create script
for each project name. It's purpose is to generate and copy source tarball to
SOURCES/ directory. Typical script looks like:

    $ cat .git/sbu-sources/katello-selinux
    #!/bin/bash
    DIR=$HOME/work/$(basename $0)
    pushd $DIR
    rake pkg:generate_source
    popd
    mv -v $DIR/pkg/*.tar.{bz2,gz} $HOME/rpmbuild/SOURCES/ 2>/dev/null

You'll also need an alias `kojikat` to point to:

    koji -c ~/.koji/katello-config build

## HOWTO: create a new core package or dependency

1. Check if it's available in Fedora:
  * https://apps.fedoraproject.org/packages/NAME
  * http://www.isitfedoraruby.com/fedorarpms/NAME
  * If only building non-SCL and it's in both Fedora and EPEL, stop now
1. If available in Fedora, copy the spec from the SCM link on the left
1. Copy the template/ directory
  1. rename the spec file, don't use an SCL prefix
  1. update gem\_name, version, ensure "Release" is 1
  1. empty the %changelog section
  1. express all gem dependencies as identical `Requires` in the spec file
1. Download the source file (e.g. the .gem) into the spec directory and run
   `git annex add foo.gem`
1. Update rel-eng/tito.props
  * If building for Fedora, add to the "katello-nightly-fedora19" whitelist
  * If building non-SCL *only*, add to the "katello-nightly-rhel+" blacklist
  * If building SCL EL6 only, no action required
1. Update comps/comps-katello-\*.xml
2. Run ./comps_doc.sh to automatically add docs
1. Commit the changes
  1. `git add -A`
  1. `git commit -m "Add NAME package"`
1. Follow the "test a package" section above until it builds for all
   targeted platforms and required SCL + non-SCL modes.
1. Submit a pull request against `master` branch.

## HOWTO: update a package

1. `git rm foo-old.gem`
1. Change the version in the spec, set "Release" to 1
1. Run `gem compare -b foo 0.1 0.2` (needs [gem-compare](https://rubygems.org/gems/gem-compare))
  1. update `Requires` to match changes in runtime dependencies
  1. add/remove entries in %files if required for new root files
1. Download the source file (e.g. the .gem) into the spec directory and run
   `git annex add foo.gem`
1. Commit the changes
  1. `git add -A`
  1. `git commit -m "Update NAME to VERSION"`
1. Follow the "test a package" section above until it builds for all
   targeted platforms and required SCL + non-SCL modes.
1. Submit a pull request against `master` branch.

## How does this repo work?

This repo contains a directory per source package and some tito configuration
and state (under rel-eng/).  Each source package directory contains a spec
file and patches under version control plus references to the source files
(i.e. gems or tarballs).

These references are managed using git-annex, a git extension for tracking
large binary blobs outside of the git repo itself.  This means we can
reference source files directly on rubygems.org etc, or perhaps set up a kind
of lookaside cache in the future.  For now, we use the [special web remote](http://git-annex.branchable.com/tips/using_the_web_as_a_special_remote/)
with URLs to all of our source files available on the web.

tito's git-annex support will automatically (lazily) fetch files and cache
them in your local git checkout as and when you build packages.

tito works in two key stages: tagging and releasing.  For every RPM build, a
tag needs to be created with tito (i.e. `tito tag --keep-version`) and this
git tag is pushed to the central repository.  tito helps by creating a
%changelog entry and tags in standard formats etc.

When a tag is present in the central repository for a version, tito lets you
build a SRPM and submit to koji, which builds the binary package (whereupon it
gets pulled into our yum repositories).  This tagging strategy means we can
rebuild a package from any point in the repository's history, and since the
git-annex metadata is part of the tagged commit, even the binary content is
effectively under source control.

This repository is branched like Foreman itself, with rpm/1.x branches
for major releases.

To find tito build targets do this:

    $ tito release -l
    [koji-katello]

## License

Spec files are generally based on Fedora spec files, which means that unless a
spec file contains an explicit license attribution within it, it is available
under the MIT license.
