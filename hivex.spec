# conditionalize Ocaml support
%ifarch sparc64 s390
%bcond_with ocaml
%else
%bcond_without ocaml
%endif

Name:           hivex
Version:        1.3.10
Release:        6.9%{?dist}
Summary:        Read and write Windows Registry binary hive files

License:        LGPLv2
URL:            http://libguestfs.org/

Source0:        http://libguestfs.org/download/hivex/%{name}-%{version}.tar.gz

# The RHEL 7 patches are stored in the upstream git repository,
# in the branch called 'rhel-7.4', ie:
# https://github.com/libguestfs/hivex/tree/rhel-7.4

# Fix Perl directory install path.
Patch0001:      0001-Fix-Perl-directory-install-path.patch

# Upstream patches to fix RHBZ#1145056.
Patch0002:      0002-value-Set-errno-0-on-non-error-path-in-hivex_value_d.patch
Patch0003:      0003-hivexml-Tidy-up-error-handling-and-printing.patch
Patch0004:      0004-lib-Don-t-leak-errno-from-_hivex_recode-function.patch

# Upstream patches to fix RHBZ#1158992.
Patch0005:      0005-handle-Refuse-to-open-files-8192-bytes-in-size.patch
Patch0006:      0006-handle-Check-that-pages-do-not-extend-beyond-the-end.patch

# Fix typo in documentation (RHBZ#1099286).
Patch0007:      0007-generator-Fix-a-spelling-mistake-in-the-documentatio.patch

# Tolerate corruption in some hives (RHBZ#1423436).
Patch0008:      0008-add-HIVEX_OPEN_UNSAFE-flag.patch
Patch0009:      0009-lib-change-how-hbin-sections-are-read.patch
Patch0010:      0010-lib-allow-to-walk-registry-with-corrupted-blocks.patch
Patch0011:      0011-hivexsh-add-u-flag-for-HIVEX_OPEN_UNSAFE.patch
Patch0012:      0012-hivexregedit-allow-to-pass-HIVEX_OPEN_UNSAFE.patch

# Patch generated code (because we can't assume we have OCaml on all
# arches).  To construct this you need to do 'make prep', run the
# generator by hand, and diff before and after.
Patch9999:      generated.patch

# Use git to apply patches.
BuildRequires:  git

# Since some patches touch autotools file, we need to rerun autoreconf.
BuildRequires:  autoconf, automake, libtool, gettext-devel

BuildRequires:  perl
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-IO-stringy
BuildRequires:  perl-libintl
%if %{with ocaml}
BuildRequires:  ocaml
BuildRequires:  ocaml-findlib-devel
%endif
BuildRequires:  python-devel
BuildRequires:  ruby-devel
BuildRequires:  rubygem-rake
BuildRequires:  rubygem(minitest)
BuildRequires:  readline-devel
BuildRequires:  libxml2-devel

# This library used to be part of libguestfs.  It won't install alongside
# the old version of libguestfs that included this library:
Conflicts:      libguestfs <= 1:1.0.84

# https://fedoraproject.org/wiki/Packaging:No_Bundled_Libraries#Packages_granted_exceptions
Provides:      bundled(gnulib)


%description
Hive files are the undocumented binary files that Windows uses to
store the Windows Registry on disk.  Hivex is a library that can read
and write to these files.

'hivexsh' is a shell you can use to interactively navigate a hive
binary file.

'hivexregedit' lets you export and merge to the textual regedit
format.

'hivexml' can be used to convert a hive file to a more useful XML
format.

In order to get access to the hive files themselves, you can copy them
from a Windows machine.  They are usually found in
%%systemroot%%\system32\config.  For virtual machines we recommend
using libguestfs or guestfish to copy out these files.  libguestfs
also provides a useful high-level tool called 'virt-win-reg' (based on
hivex technology) which can be used to query specific registry keys in
an existing Windows VM.

For OCaml bindings, see 'ocaml-hivex-devel'.

For Perl bindings, see 'perl-hivex'.

For Python bindings, see 'python-hivex'.

For Ruby bindings, see 'ruby-hivex'.


%package devel
Summary:        Development tools and libraries for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig


%description devel
%{name}-devel contains development tools and libraries
for %{name}.


%if %{with ocaml}
%package -n ocaml-%{name}
Summary:       OCaml bindings for %{name}
Requires:      %{name} = %{version}-%{release}


%description -n ocaml-%{name}
ocaml-%{name} contains OCaml bindings for %{name}.

This is for toplevel and scripting access only.  To compile OCaml
programs which use %{name} you will also need ocaml-%{name}-devel.


%package -n ocaml-%{name}-devel
Summary:       OCaml bindings for %{name}
Requires:      ocaml-%{name} = %{version}-%{release}


%description -n ocaml-%{name}-devel
ocaml-%{name}-devel contains development libraries
required to use the OCaml bindings for %{name}.
%endif


%package -n perl-%{name}
Summary:       Perl bindings for %{name}
Requires:      %{name} = %{version}-%{release}
Requires:      perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))


%description -n perl-%{name}
perl-%{name} contains Perl bindings for %{name}.


%package -n python-%{name}
Summary:       Python bindings for %{name}
Requires:      %{name} = %{version}-%{release}

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%description -n python-%{name}
python-%{name} contains Python bindings for %{name}.


%package -n ruby-%{name}
Summary:       Ruby bindings for %{name}
Requires:      %{name} = %{version}-%{release}
Requires:      ruby(release)
Requires:      ruby
Provides:      ruby(hivex) = %{version}

%description -n ruby-%{name}
ruby-%{name} contains Ruby bindings for %{name}.


%prep
%setup -q

# Use git to apply patches.
# http://rwmj.wordpress.com/2011/08/09/nice-rpm-git-patch-management-trick/
git init
git config user.email "libguestfs@redhat.com"
git config user.name "libguestfs"
git add .
git commit -a -q -m "%{version} baseline"
for f in %{patches}; do
    if [[ ! "$f" =~ generated.patch ]]; then
	git am "$f"
    else
	patch -p1 < "$f"
    fi
done

autoreconf -i

%build
%configure --disable-static
make V=1 INSTALLDIRS=vendor %{?_smp_mflags}


%check
make check

%if !%{with ocaml}
# Delete OCaml files, in case the user had OCaml installed and it was
# picked up by the configure script.
# XXX Add ./configure --disable-ocaml upstream.
rm -rf $RPM_BUILD_ROOT%{_libdir}/ocaml/hivex
rm -f  $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs/*hivex*
%endif


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALLDIRS=vendor

# Remove unwanted libtool *.la file:
rm $RPM_BUILD_ROOT%{_libdir}/libhivex.la

# Remove unwanted Perl files:
find $RPM_BUILD_ROOT -name perllocal.pod -delete
find $RPM_BUILD_ROOT -name .packlist -delete
find $RPM_BUILD_ROOT -name '*.bs' -delete

# Remove unwanted Python files:
rm $RPM_BUILD_ROOT%{python_sitearch}/libhivexmod.la

%find_lang %{name}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f %{name}.lang
%doc README LICENSE
%{_bindir}/hivexget
%{_bindir}/hivexml
%{_bindir}/hivexregedit
%{_bindir}/hivexsh
%{_libdir}/libhivex.so.*
%{_mandir}/man1/hivexget.1*
%{_mandir}/man1/hivexml.1*
%{_mandir}/man1/hivexregedit.1*
%{_mandir}/man1/hivexsh.1*


%files devel
%doc LICENSE
%{_libdir}/libhivex.so
%{_mandir}/man3/hivex.3*
%{_includedir}/hivex.h
%{_libdir}/pkgconfig/hivex.pc


%if %{with ocaml}
%files -n ocaml-%{name}
%doc README
%{_libdir}/ocaml/hivex
%exclude %{_libdir}/ocaml/hivex/*.a
%exclude %{_libdir}/ocaml/hivex/*.cmxa
%exclude %{_libdir}/ocaml/hivex/*.cmx
%exclude %{_libdir}/ocaml/hivex/*.mli
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner


%files -n ocaml-%{name}-devel
%{_libdir}/ocaml/hivex/*.a
%{_libdir}/ocaml/hivex/*.cmxa
%{_libdir}/ocaml/hivex/*.cmx
%{_libdir}/ocaml/hivex/*.mli
%endif


%files -n perl-%{name}
%{perl_vendorarch}/*
%{_mandir}/man3/Win::Hivex.3pm*
%{_mandir}/man3/Win::Hivex::Regedit.3pm*


%files -n python-%{name}
%{python_sitearch}/*.py
%{python_sitearch}/*.pyc
%{python_sitearch}/*.pyo
%{python_sitearch}/*.so


%files -n ruby-%{name}
%doc ruby/doc/site/*
%{ruby_vendorlibdir}/hivex.rb
%{ruby_vendorarchdir}/_hivex.so


%changelog
* Tue Oct 10 2017 Richard W.M. Jones <rjones@redhat.com> - 1.3.10-6.9
- Enable OCaml subpackage on s390x.
  resolves: rhbz#1447983

* Fri Sep 22 2017 Richard W.M. Jones <rjones@redhat.com> - 1.3.10-6.8
- Rebuild for OCaml 4.05
  resolves: rhbz#1447983

* Fri Feb 17 2017 Richard W.M. Jones <rjones@redhat.com> - 1.3.10-5.8
- Tolerate corruption in some hives
  resolves: rhbz#1423436
- Switch to using git to manage patches.

* Mon Nov 17 2014 Richard W.M. Jones <rjones@redhat.com> - 1.3.10-5.7
- Fix: "Argument list too long" when using virt-v2v on Windows guest
  with French copy of Citrix installed
  related: rhbz#1145056

* Mon Nov 17 2014 Richard W.M. Jones <rjones@redhat.com> - 1.3.10-5.6
- Fix: typo in man page
  resolves: rhbz#1099286

* Thu Nov 13 2014 Richard W.M. Jones <rjones@redhat.com> - 1.3.10-5.4
- Fix: hivex missing checks for small/truncated files
  resolves: rhbz#1158992

* Wed Sep 24 2014 Richard W.M. Jones <rjones@redhat.com> - 1.3.10-5.3
- Fix: hivexml generates "Argument list too long" error.
  resolves: rhbz#1145056

* Fri Aug 08 2014 Richard W.M. Jones <rjones@redhat.com> - 1.3.10-5.2
- Resolves: rhbz#1125544

* Mon Jul 21 2014 Richard W.M. Jones <rjones@redhat.com> - 1.3.10-5.1
- Rebase to hivex 1.3.10.
  resolves: rhbz#1023978

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.3.8-4
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.3.8-3
- Mass rebuild 2013-12-27

* Thu Oct 31 2013 Richard W.M. Jones <rjones@redhat.com> - 1.3.8-2
- Drop hivex-static subpackage
  resolves: rhbz#1020019

* Thu Jul 25 2013 Richard W.M. Jones <rjones@redhat.com> - 1.3.8-1
- New upstream version 1.3.8.
- Fixes handling of keys which use ri-records, for both reading and
  writing (RHBZ#717583, RHBZ#987463).
- Remove upstream patch.
- Rebase dirs patch against new upstream sources.
- Rebase ruby patch against new upstream sources.
- Modernize the RPM spec file.
- Fix .gitignore.

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.3.7-8
- Perl 5.18 rebuild

* Wed Mar 13 2013 Richard W.M. Jones <rjones@redhat.com> - 1.3.7-7
- Rebuild for Ruby 2.0.0.
- Change ruby(abi) to ruby(release).

* Fri Feb 15 2013 Richard W.M. Jones <rjones@redhat.com> - 1.3.7-6
- Fix for latest Ruby in Rawhide.  Fixes build failure identified
  by mass rebuild yesterday.
- Do not ignore error from running autoreconf.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 29 2012 Richard W.M. Jones <rjones@redhat.com> - 1.3.7-2
- Rebuild for OCaml 4.00.1.

* Thu Oct 11 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.7-1
- New upstream version 1.3.7.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 27 2012 Petr Pisar <ppisar@redhat.com> - 1.3.6-2
- Perl 5.16 rebuild

* Tue Jun 12 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.6-1
- New upstream version 1.3.6.
- Enable Ocaml bindings on ppc64.

* Sat Jun 09 2012 Richard W.M. Jones <rjones@redhat.com> - 1.3.5-9
- Rebuild for OCaml 4.00.0.

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 1.3.5-8
- Perl 5.16 rebuild

* Fri May 18 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.5-7
- "blobs" -> "files" in the description.

* Tue May 15 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.5-6
- Bundled gnulib (RHBZ#821763).

* Fri Mar 23 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.5-5
- Don't need to rerun the generator (thanks Dan Horák).

* Tue Mar 13 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.5-4
- New upstream version 1.3.5.
- Remove upstream patch.
- Depend on automake etc. for the patch.

* Thu Feb  9 2012 Richard W.M. Jones <rjones@redhat.com> - 1.3.3-8
- ruby(abi) 1.9.1.

* Wed Feb  8 2012 Richard W.M. Jones <rjones@redhat.com> - 1.3.3-7
- Bump and rebuild for Ruby update.
- Add upstream patch to fix bindings for Ruby 1.9.
- Add non-upstream patch to pass --vendor flag to extconf.rb

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 1.3.3-3
- Rebuild for OCaml 3.12.1.

* Thu Dec  8 2011 Richard W.M. Jones <rjones@redhat.com> - 1.3.3-2
- Disable OCaml on ppc64.
- Ensure OCaml files are deleted when not packaged.

* Tue Nov 29 2011 Richard W.M. Jones <rjones@redhat.com> - 1.3.3-1
- New upstream version 1.3.3.
- Rebased gnulib to work around RHBZ#756981.
- Remove patches which are now upstream.

* Mon Oct 24 2011 Richard W.M. Jones <rjones@redhat.com> - 1.3.2-3
- New upstream version 1.3.2.
- Add upstream patch to fix building of hivexsh, hivexget.

* Fri Aug 26 2011 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-2
- New upstream version 1.3.1.
- Remove patch, now upstream.
- Don't need hack for making an unversioned Python module.

* Mon Aug 15 2011 Richard W.M. Jones <rjones@redhat.com> - 1.3.0-3
- New upstream version 1.3.0.
- This version adds Ruby bindings, so there is a new subpackage 'ruby-hivex'.
- Add upstream patch to fix Ruby tests.
- Remove epoch macro in ruby-hivex dependency.

* Fri Aug 12 2011 Richard W.M. Jones <rjones@redhat.com> - 1.2.8-1
- New upstream version 1.2.8.
- Remove 4 upstream patches.

* Fri Jul 22 2011 Richard W.M. Jones <rjones@redhat.com> - 1.2.7-9
- Add upstream patch to fix Perl CCFLAGS for Perl 5.14 on i686.
- Enable 'make check'.

* Thu Jul 21 2011 Richard W.M. Jones <rjones@redhat.com> - 1.2.7-6
- i686 package is broken, experimentally rebuild it.

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.2.7-5
- Perl mass rebuild

* Fri Jun 10 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.2.7-4
- Perl 5.14 mass rebuild

* Tue May 17 2011 Richard W.M. Jones <rjones@redhat.com> - 1.2.7-3
- New upstream version 1.2.7.
- Removed patch which is now upstream.
- Add upstream patches to fix ocaml install rule.

* Thu May 12 2011 Richard W.M. Jones <rjones@redhat.com> - 1.2.6-2
- New upstream version 1.2.6.
- Removed patch which is now upstream.
- Add upstream patch to fix ocaml tests.

* Thu Apr 28 2011 Richard W.M. Jones <rjones@redhat.com> - 1.2.5-2
- Fix Python bindings on 32 bit arch with upstream patch.

* Wed Apr 13 2011 Richard W.M. Jones <rjones@redhat.com> - 1.2.5-1
- New upstream version 1.2.5.
- This version fixes a number of important memory issues found by
  valgrind and upgrading to this version is recommended for all users.
- Remove patch now upstream.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 14 2011 Richard W.M. Jones <rjones@redhat.com> - 1.2.4-6
- Fix multilib conflicts in *.pyc and *.pyo files.
- Only install unversioned *.so file for Python bindings.

* Wed Jan  5 2011 Richard W.M. Jones <rjones@redhat.com> - 1.2.4-4
- Rebuild against OCaml 3.12.0.

* Thu Dec 16 2010 Richard W.M. Jones <rjones@redhat.com> - 1.2.4-3
- Backport upstream patch to fix segfault in Hivex.value_value binding.

* Thu Dec  2 2010 Richard W.M. Jones <rjones@redhat.com> - 1.2.4-1
- New upstream version 1.2.4.
- This adds Python bindings (python-hivex subpackage).
- Fix Source0.

* Fri Nov 19 2010 Dan Horák <dan[at]danny.cz> - 1.2.3-3
- fix built with recent perl

* Tue Sep  7 2010 Dan Horák <dan[at]danny.cz> - 1.2.3-2
- conditionalize ocaml support

* Fri Aug 27 2010 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-1
- New upstream version 1.2.3.

* Wed Aug 25 2010 Richard W.M. Jones <rjones@redhat.com> - 1.2.2-3
- Create a hivex-static subpackage.

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.2.2-2
- Mass rebuild with perl-5.12.0

* Wed Apr 28 2010 Richard W.M. Jones <rjones@redhat.com> - 1.2.2-1
- New upstream version 1.2.2.

* Tue Mar 30 2010 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-1
- New upstream version 1.2.1.
- Includes new tool for exporting and merging in regedit format.

* Mon Mar  1 2010 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-2
- New upstream version 1.2.0.
- This includes OCaml and Perl bindings, so add these as subpackages.

* Mon Feb 22 2010 Richard W.M. Jones <rjones@redhat.com> - 1.1.2-3
- Missing Epoch in conflicts version fixed.

* Mon Feb 22 2010 Richard W.M. Jones <rjones@redhat.com> - 1.1.2-2
- Add Conflicts libguestfs <= 1.0.84.

* Mon Feb 22 2010 Richard W.M. Jones <rjones@redhat.com> - 1.1.2-1
- Initial Fedora RPM.
