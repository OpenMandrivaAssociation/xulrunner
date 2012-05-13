#
# WARNING, READ FIRST:
#
# This is a special package that needs special treatment. Due to the amount of
# security updates it needs, it's common to ship new upstream versions instead of patching.
# That means this package MUST be BUILDABLE for stable official releases.
# This also means only STABLE upstream releases, NO betas.
# This is a discussed topic. Please, do not flame it again.

# (tpg) DO NOT FORGET TO SET EXACT XULRUNNER and FIREFOX VERSIONS !
%define ffver 12.0
%define version_internal 12.0

# (tpg) define release here
%if %mandriva_branch == Cooker
# Cooker
%define release 1
%else
# Old distros
%define subrel 1
%define release %mkrel 0
%endif

# (tpg) DO NOT FORGET TO SET EXACT MAJOR!
# in this case %{major} == %{version_internal}
%define major %{version_internal}
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d
%define develunstname %mklibname %{name}-unstable -d
%define sname firefox

# (tpg) various directory defines
%define mozappdir %{_libdir}/%{name}-%{version_internal}

%define nss_libname %mklibname nss 3
%define nspr_libname %mklibname nspr 4

# this seems fragile, so require the exact version or later (#58754)
%define sqlite3_version %(pkg-config --modversion sqlite3 &>/dev/null && pkg-config --modversion sqlite3 2>/dev/null || echo 0)
%define nss_version %(pkg-config --modversion nss &>/dev/null && pkg-config --modversion nss 2>/dev/null || echo 0)

%define _use_syshunspell 1

Summary:	XUL Runtime for Gecko Applications
Name:		xulrunner
Version:	%{version_internal}
Release:	%{release}
License:	MPLv1.1 or GPLv2+ or LGPLv2+
Group:		Development/Other
Url:		http://developer.mozilla.org/en/docs/XULRunner
Source0:	ftp://ftp.mozilla.org/pub/mozilla.org/%{sname}/releases/%{ffver}/source/%{sname}-%{ffver}.source.tar.bz2
Patch0:		mozilla-nongnome-proxies.patch
Patch1:		xulrunner-9.0-pluginsdir2.patch
Patch2:		xulrunner-1.9.0.1-version.patch
Patch3:		xulrunner-2.0-pkgconfig.patch
Patch4:		xulrunner-1.9.2-public-opearator-delete.patch
# https://bugzilla.mozilla.org/show_bug.cgi?id=722975
Patch5:		firefox_add_ifdefs_to_gfx_thebes_gfxPlatform.cpp.patch

BuildRequires:	doxygen
BuildRequires:	java-rpmbuild
BuildRequires:	makedepend
BuildRequires:	valgrind
BuildRequires:	python
BuildRequires:	rootcerts
BuildRequires:	unzip
BuildRequires:	yasm >= 1.0.1
BuildRequires:	zip
BuildRequires:	bzip2-devel
BuildRequires:	nss-static-devel >= 2:3.13.3
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libevent) >= 1.4.7
BuildRequires:	pkgconfig(libgnomeui-2.0)
BuildRequires:	pkgconfig(libIDL-2.0)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(libproxy-1.0) >= 0.4.4
BuildRequires:	pkgconfig(libstartup-notification-1.0)
BuildRequires:	pkgconfig(nspr)
BuildRequires:	pkgconfig(nss)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(sqlite3) >= 3.7.7.1
BuildRequires:	pkgconfig(vpx) >= 0.9.7
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(zlib)
%if %_use_syshunspell
BuildRequires:	pkgconfig(hunspell)
%endif
%if %mdkversion > 201100
BuildRequires:	pkgconfig(cairo) >= 1.10
BuildRequires:	pkgconfig(libpng) >= 1.4.8
BuildRequires:	pkgconfig(valgrind)
%else
BuildRequires:	gnome-vfs2-devel
%endif

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
Requires:	%{mklibname sqlite3_ 0} >= %{sqlite3_version}
# (salem) bug #42680 for noarch packages
Provides:	libxulrunner = %{version}-%{release}

%description -n %{libname}
Dynamic libraries for %{name}.

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}
Requires:	nss-devel >= 2:%{nss_version}
Obsoletes:	xulrunner-devel < 1.9.2
Provides:	%{name}-devel = %{version}-%{release}
# (tpg) see above why

%description -n %{develname}
Development files and headers for %{name}.

%prep

%setup -qn mozilla-release
%patch0 -p0 -b .nongnome-proxies
%patch1 -p1 -b .pluginsdir2
%patch2 -p1 -b .version
%patch3 -p1 -b .pkgconfig
%patch4 -p1 -b .public-opearator-delete
%patch5 -p1

#(tpg) correct the xulrunner version
sed -i -e 's#INTERNAL_VERSION#%{version_internal}#g' xulrunner/installer/Makefile.in

%build
# (gmoro) please dont enable all options by hand
# we need to trust firefox defaults
export MOZCONFIG=`pwd`/mozconfig
cat << EOF > $MOZCONFIG
mk_add_options MOZILLA_OFFICIAL=1
mk_add_options BUILD_OFFICIAL=1
#mk_add_options MOZ_MAKE_FLAGS="%{_smp_mflags}"
mk_add_options MOZ_OBJDIR=@TOPSRCDIR@
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
%if %mdkversion >= 201100
ac_add_options --with-system-png
ac_add_options --enable-system-cairo
ac_add_options --enable-gio
ac_add_options --disable-gnomevfs
%else
ac_add_options --disable-system-png
ac_add_options --disable-system-cairo
ac_add_options --enable-gnomevfs
%endif
ac_add_options --with-system-bz2
ac_add_options --enable-system-sqlite
%if %_use_syshunspell
ac_add_options --enable-system-hunspell
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
ac_add_options --enable-chrome-format=jar
ac_add_options --with-distribution-id=com.mandriva
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
%ifarch %{ix86} x86_64
[ -z "$RPM_BUILD_NCPUS" ] && \
     RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"
[ "$RPM_BUILD_NCPUS" -ge 2 ] && MOZ_SMP_FLAGS=-j2
[ "$RPM_BUILD_NCPUS" -ge 4 ] && MOZ_SMP_FLAGS=-j4
%endif

export LDFLAGS="%{ldflags}"
make -f client.mk build STRIP="/bin/true" MOZ_MAKE_FLAGS="$MOZ_SMP_FLAGS" MOZ_SERVICES_SYNC="1"

%install
%makeinstall_std STRIP=/bin/true

rm -rf %{buildroot}%{_libdir}/%{name}-devel-%{version_internal}/sdk/lib/*.so
pushd %{buildroot}%{mozappdir}
for i in *.so; do
    ln -s %{mozappdir}/$i %{buildroot}%{_libdir}/%{name}-devel-%{version_internal}/sdk/lib/$i
done
popd

# Copy pc files needed by eclipse
%{__cp} %{buildroot}/%{_libdir}/pkgconfig/libxul.pc \
         %{buildroot}/%{_libdir}/pkgconfig/libxul-unstable.pc
%{__cp} %{buildroot}/%{_libdir}/pkgconfig/libxul-embedding.pc \
         %{buildroot}/%{_libdir}/pkgconfig/libxul-embedding-unstable.pc

# Don't install these in appdir
rm  %{buildroot}%{mozappdir}/LICENSE
rm  %{buildroot}%{mozappdir}/README.txt

%if %_use_syshunspell
# Use the system hunspell dictionaries
rm -rf %{buildroot}%{mozappdir}/dictionaries
ln -s %{_datadir}/dict/mozilla %{buildroot}%{mozappdir}/dictionaries
%endif

# ghost files
mkdir -p %{buildroot}%{mozappdir}/components
touch %{buildroot}%{mozappdir}/components/compreg.dat
touch %{buildroot}%{mozappdir}/components/xpti.dat

# set up our default preferences
cat << EOF > %{buildroot}%{mozappdir}/defaults/pref/vendor.js
pref("general.useragent.vendor", "%{distribution}");
pref("general.useragent.vendorSub", "%{version}-%{release}");
pref("general.useragent.vendorComment", "%{mandriva_release}");
pref("general.smoothScroll", true);
pref("mousewheel.horizscroll.withnokey.action", 0);
pref("mousewheel.horizscroll.withnokey.numlines", 3);
pref("mousewheel.horizscroll.withnokey.sysnumlines", false);
pref("mousewheel.withnokey.action", 0);
pref("mousewheel.withnokey.numlines", 7);
pref("mousewheel.withnokey.sysnumlines", false);
pref("network.protocol-handler.app.mailto", "/usr/bin/xdg-email");
pref("network.protocol-handler.app.mms", "/usr/bin/xdg-open");
pref("network.http.pipelining", true);
pref("network.http.proxy.pipelining", true);
pref("network.http.pipelining.maxrequests", 8);
pref("browser.display.use_system_colors", true);
pref("browser.tabs.loadDivertedInBackground", true);
pref("browser.startup.homepage_override.mstone", "ignore");
pref("browser.backspace_action", 2);
pref("browser.tabs.loadFolderAndReplace", false);
pref("browser.EULA.override", true);
pref("browser.safebrowsing.enabled", true);
pref("browser.shell.checkDefaultBrowser", false);
pref("browser.startup.homepage", "file:///usr/share/doc/HTML/index.html");
pref("browser.ctrlTab.previews", true);
pref("browser.tabs.insertRelatedAfterCurrent", false);
pref("print.print_edge_top", 14); // 1/100 of an inch
pref("print.print_edge_left", 16); // 1/100 of an inch
pref("print.print_edge_right", 16); // 1/100 of an inch
pref("print.print_edge_bottom", 14); // 1/100 of an inch
pref("app.update.enabled", false);
pref("app.update.auto", false);
pref("app.update.autoInstallEnabled", false);
pref("intl.locale.matchOS", true);
pref("toolkit.storage.synchronous", 0);
pref("layout.css.visited_links_enabled", false);
pref("security.ssl.require_safe_negotiation", false);
EOF

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
%{mozappdir}/components/*.xpt
%{mozappdir}/components/*.manifest
%{mozappdir}/*.manifest
%attr(644, root, root) %{mozappdir}/components/*.js
%{mozappdir}/defaults
%{mozappdir}/modules
%{mozappdir}/plugins
%{mozappdir}/res
%{mozappdir}/*.so
%{mozappdir}/mozilla-xremote-client
%{mozappdir}/run-mozilla.sh
%{mozappdir}/greprefs.js
%{mozappdir}/xulrunner
%{mozappdir}/xulrunner-bin
%{mozappdir}/xulrunner-stub
%{mozappdir}/platform.ini
%{mozappdir}/dependentlibs.list
%{mozappdir}/plugin-container
%{mozappdir}/hyphenation

%files -n %{develname}
%{_includedir}/%{name}-%{version_internal}
%{mozappdir}/xpcshell
%{_libdir}/%{name}-devel-%{version_internal}
%{_libdir}/pkgconfig/*.pc
%{_datadir}/idl/%{name}-%{version_internal}
%{_sys_macros_dir}/%{name}.macros
