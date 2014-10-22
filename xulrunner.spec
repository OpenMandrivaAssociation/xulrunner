#
# WARNING, READ FIRST:
#
# This is a special package that needs special treatment. Due to the amount of
# security updates it needs, it's common to ship new upstream versions instead of patching.
# That means this package MUST be BUILDABLE for stable official releases.
# This also means only STABLE upstream releases, NO betas.
# This is a discussed topic. Please, do not flame it again.

# (tpg) DO NOT FORGET TO SET EXACT XULRUNNER and FIREFOX VERSIONS !
%define ffver 28.0
%define version_internal 28.0

# (tpg) DO NOT FORGET TO SET EXACT MAJOR!
# in this case %{major} == %{version_internal}
%define major %{version_internal}
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d
%define develunstname %mklibname %{name}-unstable -d
%define sname firefox

# (tpg) various directory defines
%define mozappdir %{_libdir}/%{name}

%define nss_libname %mklibname nss 3
%define nspr_libname %mklibname nspr 4

# this seems fragile, so require the exact version or later (#58754)
%define sqlite3_version %(pkg-config --modversion sqlite3 &>/dev/null && pkg-config --modversion sqlite3 2>/dev/null || echo 0)
%define nss_version %(pkg-config --modversion nss &>/dev/null && pkg-config --modversion nss 2>/dev/null || echo 0)

%define _use_syshunspell 1

Summary:	XUL Runtime for Gecko Applications
Name:		xulrunner
Version:	%{version_internal}
Release:	4
License:	MPLv1.1 or GPLv2+ or LGPLv2+
Group:		Development/Other
Url:		http://developer.mozilla.org/en/docs/XULRunner
Source0:	ftp://ftp.mozilla.org/pub/mozilla.org/%{sname}/releases/%{ffver}/source/%{sname}-%{ffver}.source.tar.bz2
Source1:	xulrunner-omv-default-prefs.js
Source2:	xulrunner.rpmlintrc
# build patches
Patch1:         xulrunner-install-dir.patch
Patch2:         mozilla-build.patch
Patch3:         mozilla-build-arm.patch
Patch14:        xulrunner-2.0-chromium-types.patch
Patch17:        xulrunner-24.0-gcc47.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=814879#c3
Patch18:        xulrunner-24.0-jemalloc-ppc.patch
# workaround linking issue on s390 (JSContext::updateMallocCounter(size_t) not found)
Patch19:        xulrunner-24.0-s390-inlines.patch
Patch20:	firefox-28.0-nss_detect.patch

# Fedora specific patches
Patch200:        mozilla-193-pkgconfig.patch
# Unable to install addons from https pages
Patch204:        rhbz-966424.patch

# Upstream patches
Patch300:        mozilla-837563.patch
Patch301:        mozilla-938730.patch

BuildRequires:	autoconf2.1
BuildRequires:	zlib-devel
BuildRequires:	bzip2-devel
BuildRequires:	pkgconfig(libpng) >= 1.4.8
%if %_use_syshunspell
BuildRequires:	hunspell-devel
%endif
BuildRequires:	pkgconfig(vpx) >= 0.9.7
BuildRequires:	pkgconfig(libIDL-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(xt)
BuildRequires:	startup-notification-devel >= 0.8
BuildRequires:	dbus-glib-devel
BuildRequires:	pkgconfig(libevent) >= 1.4.7
BuildRequires:	sqlite3-devel >= 3.7.7.1
BuildRequires:	gnome-vfs2-devel
BuildRequires:	pkgconfig(libgnome-2.0)
BuildRequires:	pkgconfig(libgnomeui-2.0)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	java-rpmbuild
BuildRequires:	java-devel-openjdk
BuildRequires:	unzip
BuildRequires:	zip
BuildRequires:	doxygen
BuildRequires:	makedepend
BuildRequires:	valgrind
BuildRequires:	libiw-devel
BuildRequires:	valgrind-devel
BuildRequires:	rootcerts
BuildRequires:	python
BuildRequires:  nspr-devel >= 2:4.9.0
BuildRequires:  nss-devel >= 2:3.13.3
BuildRequires:  nss-static-devel >= 2:3.13.3
BuildRequires:	pango-devel
BuildRequires:	libalsa-devel
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(osmesa)
BuildRequires:	cairo-devel >= 1.10
BuildRequires:	yasm >= 1.0.1
BuildRequires:	pkgconfig(libproxy-1.0) >= 0.4.4
BuildRequires:	python-distribute
BuildRequires:	python-virtualenv
Requires:	%{libname} = %{version}-%{release}
Conflicts:	xulrunner < %{version}

%description
XULRunner is a Mozilla runtime package that can be used to
bootstrap XUL+XPCOM applications that are as rich as Firefox
and Thunderbird. It will provide mechanisms for installing,
upgrading, and uninstalling these applications. XULRunner will
also provide libxul, a solution which allows the embedding of
Mozilla technologies in other projects and products.

%package -n %{libname}
Summary:        Dynamic libraries for %{name}
Group:          System/Libraries
Conflicts:	xulrunner < %{version}
Obsoletes:	%{mklibname xulrunner 1.9.2} < %{version}-%{release}
Requires:	rootcerts
# (tpg) manually pull dependancies on libnss3 and libnspr4, why ? see above
Requires:	%{nss_libname} >= 2:%{nss_version}
Requires:	%{nspr_libname} >= 2:4.9.0
# (salem) bug #42680 for noarch packages
Provides:	libxulrunner = %{version}-%{release}
Requires:	%{mklibname sqlite3_ 0} >= %{sqlite3_version}

%description -n %{libname}
Dynamic libraries for %{name}.

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}
Obsoletes:	xulrunner-devel < 1.9.2
Obsoletes:	%{mklibname mozilla-firefox -d} < 0:3
Obsoletes:	%{mklibname %{name}-unstable -d}
Provides:	%{name}-devel = %{version}-%{release}
# (tpg) see above why
Requires:	nss-devel >= 2:%{nss_version}

%description -n %{develname}
Development files and headers for %{name}.

%prep

%setup -qn mozilla-release
%patch1  -p1
#patch2  -p2 -b .bld
%patch3  -p2 -b .arm
%patch14 -p2 -b .chromium-types
%patch17 -p1 -b .gcc47
%patch18 -p2 -b .jemalloc-ppc
%patch19 -p2 -b .s390-inlines
%patch20 -p1 -b .nss_detect
%patch200 -p2 -b .pk
%patch204 -p1 -b .966424
#patch300 -p1 -b .837563
#patch301 -p1 -b .938730

%build
# (gmoro) please dont enable all options by hand
# we need to trust firefox defaults
export MOZCONFIG=`pwd`/mozconfig
cat << EOF > $MOZCONFIG
mk_add_options MOZILLA_OFFICIAL=1
mk_add_options BUILD_OFFICIAL=1
#mk_add_options MOZ_MAKE_FLAGS="%{_smp_mflags}"
#mk_add_options MOZ_OBJDIR=@TOPSRCDIR@
mk_add_options MOZ_OBJDIR=`pwd`/objdir
ac_add_options --prefix="%{_prefix}"
ac_add_options --libdir="%{_libdir}"
ac_add_options --sysconfdir="%{_sysconfdir}"
ac_add_options --mandir="%{_mandir}"
ac_add_options --includedir="%{_includedir}"
ac_add_options --datadir="%{_datadir}"
ac_add_options --enable-application=xulrunner
ac_add_options --with-pthreads
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --with-system-jpeg
ac_add_options --with-system-zlib
ac_add_options --with-system-libevent
ac_add_options --with-system-libvpx
ac_add_options --with-system-png
ac_add_options --with-system-bz2
ac_add_options --enable-system-sqlite
ac_add_options --enable-system-cairo
%if %_use_syshunspell
ac_add_options --enable-system-hunspell
%endif
%ifarch armv7hl
ac_add_options --with-arch=armv7-a
ac_add_options --with-float-abi=hard
ac_add_options --with-fpu=vfpv3-d16
ac_add_options --disable-elf-hack
%endif
%ifarch armv7l
ac_add_options --with-arch=armv7-a
ac_add_options --with-float-abi=soft
ac_add_options --with-fpu=vfpv3-d16
ac_add_options --disable-elf-hack
%endif
ac_add_options --disable-javaxpcom
ac_add_options --enable-pango
ac_add_options --enable-svg
ac_add_options --enable-canvas
ac_add_options --enable-crypto
ac_add_options --disable-crashreporter
ac_add_options --disable-installer
ac_add_options --disable-updater
ac_add_options --enable-optimize
ac_add_options --enable-jemalloc
ac_add_options --disable-wrap-malloc
ac_add_options --enable-valgrind
ac_add_options --disable-strip
ac_add_options --enable-install-strip
ac_add_options --enable-startup-notification
ac_add_options --enable-default-toolkit=cairo-gtk2
ac_add_options --enable-shared-js
ac_add_options --with-java-include-path=%{java_home}/include
ac_add_options --with-java-bin-path=%{java_home}/bin
ac_add_options --enable-image-encoder=all
ac_add_options --enable-image-decoders=all
ac_add_options --enable-places
ac_add_options --enable-storage
ac_add_options --enable-safe-browsing
ac_add_options --enable-url-classifier
ac_add_options --enable-gio
ac_add_options --disable-gnomevfs
ac_add_options --enable-gnomeui
ac_add_options --disable-faststart
ac_add_options --enable-smil
ac_add_options --disable-tree-freetype
ac_add_options --enable-canvas3d
ac_add_options --disable-coretext
ac_add_options --enable-extensions=default
ac_add_options --enable-necko-protocols=all
ac_add_options --disable-necko-wifi
ac_add_options --disable-tests
ac_add_options --disable-mochitest
ac_add_options --enable-xtf
ac_add_options --enable-wave
ac_add_options --enable-ogg
ac_add_options --enable-xpcom-fastload
ac_add_options --enable-dbus
ac_add_options --enable-libproxy
ac_add_options --enable-chrome-format=omni
ac_add_options --with-distribution-id=org.openmandriva
ac_add_options --enable-pulseaudio
ac_add_options --enable-xinerama
ac_add_options --disable-gstreamer
ac_add_options --disable-cpp-exceptions
EOF

# Mozilla builds with -Wall with exception of a few warnings which show up
# everywhere in the code; so, don't override that.
#
# Disable C++ exceptions since Mozilla code is not exception-safe
#
MOZ_OPT_FLAGS=$(echo "$RPM_OPT_FLAGS" | sed -e 's/-Wall//' -e 's/-fexceptions/-fno-exceptions/g')
export CFLAGS="$MOZ_OPT_FLAGS"
export CXXFLAGS="$MOZ_OPT_FLAGS"
export PREFIX="%{_prefix}"
export LIBDIR="%{_libdir}"

MOZ_SMP_FLAGS=-j1
# On x86 architectures, Mozilla can build up to 4 jobs at once in parallel,
# however builds tend to fail on other arches when building in parallel.
%ifarch %{ix86} x86_64 %arm
[ -z "$RPM_BUILD_NCPUS" ] && \
     RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"
[ "$RPM_BUILD_NCPUS" -ge 4 ] && MOZ_SMP_FLAGS=-j4
[ "$RPM_BUILD_NCPUS" -ge 8 ] && MOZ_SMP_FLAGS=-j8
[ "$RPM_BUILD_NCPUS" -ge 16 ] && MOZ_SMP_FLAGS=-j16
%endif

export LDFLAGS="%{ldflags}"
make -f client.mk build STRIP="/bin/true" MOZ_MAKE_FLAGS="$MOZ_SMP_FLAGS -g0" MOZ_SERVICES_SYNC="1"

%install
# set up our prefs before install, so it gets pulled in to omni.jar
%{__cp} -p %{SOURCE1} objdir/dist/bin/defaults/pref/vendor.js

%makeinstall_std -C objdir STRIP=/bin/true MOZ_PKG_FATAL_WARNINGS=0

# Link libraries in sdk directory instead of copying them:
pushd $RPM_BUILD_ROOT%{_libdir}/%{name}-devel-%{version_internal}/sdk/lib/
for i in *.so; do
     rm $i
     ln -s %{mozappdir}/$i $i
done
popd

# Copy pc files needed by eclipse
%{__cp} %{buildroot}/%{_libdir}/pkgconfig/libxul.pc \
         %{buildroot}/%{_libdir}/pkgconfig/libxul-unstable.pc
%{__cp} %{buildroot}/%{_libdir}/pkgconfig/libxul-embedding.pc \
         %{buildroot}/%{_libdir}/pkgconfig/libxul-embedding-unstable.pc

# Don't install these in appdir
rm -f  %{buildroot}%{mozappdir}/LICENSE
rm -f  %{buildroot}%{mozappdir}/README.xulrunner

%if %_use_syshunspell
# Use the system hunspell dictionaries
rm -rf %{buildroot}%{mozappdir}/dictionaries
ln -s %{_datadir}/dict/mozilla %{buildroot}%{mozappdir}/dictionaries
%endif

# ghost files
mkdir -p %{buildroot}%{mozappdir}/components
touch %{buildroot}%{mozappdir}/components/compreg.dat
touch %{buildroot}%{mozappdir}/components/xpti.dat

mkdir -p %{buildroot}%{_sys_macros_dir}
cat <<FIN >%{buildroot}%{_sys_macros_dir}/%{name}.macros
# Macros from %{name} package
%%xulrunner_major            %{major}
%%xulrunner_version          %{version}
%%xulrunner_libname          %{libname}
%%xulrunner_mozappdir        %{mozappdir}
FIN

%files
%doc LICENSE README.txt
%dir %{mozappdir}
%{_bindir}/xulrunner

%files -n %{libname}
%dir %{mozappdir}
%{mozappdir}/chrome
%{mozappdir}/dictionaries
%dir %{mozappdir}/components
%ghost %{mozappdir}/components/compreg.dat
%ghost %{mozappdir}/components/xpti.dat
%{mozappdir}/components/*.so
%{mozappdir}/components/*.manifest
%{mozappdir}/*.manifest
%{mozappdir}/omni.ja
%{mozappdir}/*.so
%{mozappdir}/mozilla-xremote-client
%{mozappdir}/xulrunner
%{mozappdir}/xulrunner-stub
%{mozappdir}/platform.ini
%{mozappdir}/dependentlibs.list
%{mozappdir}/plugin-container

%files -n %{develname}
%{_includedir}/%{name}-%{ffver}
%{_libdir}/%{name}-devel-%{version_internal}
%{_libdir}/pkgconfig/*.pc
%{_datadir}/idl/%{name}-%{version_internal}
%{mozappdir}/js-gdb.py
%{_sys_macros_dir}/%{name}.macros
