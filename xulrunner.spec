#
# WARNING, READ FIRST:
#
# This is a special package that needs special treatment. Due to the amount of
# security updates it needs, it's common to ship new upstream versions instead of patching.
# That means this package MUST be BUILDABLE for stable official releases.
# This also means only STABLE upstream releases, NO betas.
# This is a discussed topic. Please, do not flame it again.

# required for, at least, 2009.0
%if %mdkversion < 200910
# (tpg) nss libraries are not conventinaly named(mozilla still sux),
# thanks to this auto dependencies are wongly generated for devel libraries
# blacklisting all nss libraries should solve this
%define _requires_exceptions libnss3\\|libnssutil3\\|libsmime3\\|libssl3\\|libnspr4\\|libplc4\\|libplds4
%endif

# (tpg) DO NOT FORGET TO SET EXACT XULRUNNER and FIREFOX VERSIONS !
%define ffver 4.0
%define version_internal 2.0

%define prel b3

# (tpg) define release here
%if %mandriva_branch == Cooker
# Cooker
%define release %mkrel -c %prel 1
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

# (salem) ugly but avoids hardcoding package versions (#42745)
# TODO: needs a better solution. (%__isa macro)?
%define hunspellver %(rpm -q --whatprovides libhunspell --queryformat %{NAME})
%define nss_libname %mklibname nss 3
%define nspr_libname %mklibname nspr 4

# this seems fragile, so require the exact version or later (#58754)
%define sqlite3_version %(pkg-config --modversion sqlite3 &>/dev/null && pkg-config --modversion sqlite3 2>/dev/null || echo 0)
%define nss_version %(pkg-config --modversion nss &>/dev/null && pkg-config --modversion nss 2>/dev/null || echo 0)

# mdv2009.0 introduced a system wide libhunspell
%if %mdkversion >= 200900
%define _use_syshunspell 1
%else
%define _use_syshunspell 0
%endif

Summary:	XUL Runtime for Gecko Applications
Name:		xulrunner
Version:	%{version_internal}
Release:	%{release}
License:	MPLv1.1 or GPLv2+ or LGPLv2+
Group:		Development/Other
Url:		http://developer.mozilla.org/en/docs/XULRunner
Source0:	ftp://ftp.mozilla.org/pub/mozilla.org/%{sname}/releases/%{ffver}/source/%{sname}-%{ffver}%prel.source.tar.bz2
Source1:	%{SOURCE0}.asc
Patch1:		xulrunner-1.9.1-max-path-len.patch
Patch5:		mozilla-nongnome-proxies.patch
Patch7:		%{name}-1.9.1-pluginsdir2.patch
# Fedora patches:
# use 1.9 as xulrunner version in the dirname and not the complete version string
Patch8:		xulrunner-1.9.0.1-version.patch
Patch9:		xulrunner-ipc-stl.patch
Patch10:	xulrunner-1.9.2-pkgconfig.patch
# (salem) this patch does not work properly on ff3
#Patch11:	xulrunner-1.9.0.1-theme-selection.patch
Patch12:	xulrunner-1.9.0.5-fix-string-format.patch
Patch14:	xulrunner-1.9.1-jemalloc.patch
Patch15:	xulrunner-1.9.1-gtk2.patch
Patch16:	xulrunner-1.9.1-java-make-j1.patch
Patch17:	xulrunner-1.9.2-public-opearator-delete.patch
Patch19:	xulrunner-1.9.2-fix-plugins-cflags.patch
Patch20:	xulrunner-1.9.2-helper-app.patch 
Patch21:	xulrunner-1.9.2-kde-integration.patch
Patch25:	xulrunner-1.9.2-realpath.patch
Patch26:	mozilla-1.9.2-gtk2.diff
BuildRequires:	zlib-devel
BuildRequires:	bzip2-devel
#(tpg) older versions doesn't support apng extension
%if %mdkversion >= 200900
BuildRequires:	libpng-devel >= 1.2.25-2
%endif
%if %_use_syshunspell
BuildRequires:	libhunspell-devel
%endif
BuildRequires:	libIDL2-devel
BuildRequires:	gtk+2-devel
BuildRequires:	startup-notification-devel
BuildRequires:	dbus-glib-devel
%if %mdkversion >= 200800
# (tpg) older releases does not have SQLITE_ENABLE_UNLOCK_NOTIFY enabled
BuildRequires:	libsqlite3-devel >= 3.7.0.1-2
%endif
BuildRequires:	libgnome-vfs2-devel
BuildRequires:	libgnome2-devel
BuildRequires:	libgnomeui2-devel
%if %mdkversion >= 200900
BuildRequires:	java-rpmbuild
%endif
%if %mdkversion < 200900
BuildRequires:	java-1.5.0-devel
%endif
BuildRequires:	zip
BuildRequires:	doxygen
BuildRequires:	makedepend
BuildRequires:	valgrind
BuildRequires:	rootcerts
BuildRequires:	python
BuildRequires:	python-devel
BuildRequires:	nspr-devel >= 2:4.8.6
BuildRequires:	nss-static-devel >= 2:3.12.7
BuildRequires:	pango-devel
BuildRequires:	libalsa-devel
BuildRequires:	libnotify-devel
BuildRequires:	mesagl-devel
%if %mdkversion >= 201000
BuildRequires:	cairo-devel >= 1.8.8
%endif
Requires:	%{libname} = %{version}-%{release}
Conflicts:	xulrunner < %{version}
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

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
Requires:	%{libname} = %{version}-%{release}
Conflicts:	xulrunner < %{version}
Obsoletes:	%{mklibname xulrunner 1.9.2} < %{version}-%{release}
Requires:	rootcerts
# (tpg) manually pull dependancies on libnss3 and libnspr4, why ? see above
Requires:	%{nss_libname} >= 2:%{nss_version}
Requires:	%{nspr_libname} >= 2:4.8.4
%if %_use_syshunspell
# (salem) fixes #42745
Requires:	%{hunspellver}
%endif
# (salem) bug #42680 for noarch packages
Provides:	libxulrunner = %{version}-%{release}
%if %mdkversion >= 200800
Requires:	%{mklibname sqlite3_ 0} >= %{sqlite3_version}
%endif

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
Requires:	nss-devel
Requires:	libalsa-devel

%description -n %{develname}
Development files and headers for %{name}.

%prep
%setup -qn mozilla-central
#%patch1 -p1 -b .pathlen rediff
%patch5 -p0 -b .proxy
%patch7 -p1 -b .plugins
%patch8 -p1 -b .version

%if %mdkversion < 200900
# patch by redhat
%patch9 -p1 -b .ipc-stl
%endif

#%patch10 -p1 -b .pkgconfig rediff
#%patch12 -p0 -b .strformat rediff
#%patch14 -p1 -b .jemalloc rediff
#%patch15 -p1 -b .gtk2
%patch16 -p1 -b .java_make-j1
%patch17 -p1
#%patch19 -p1 rediff
#%patch20 -p1 rediff
#%patch21 -p1 -b .kde-integration rediff?
%patch25 -p1

%if %mdkversion < 200900
# patch by fcrozat
%patch26 -p0
%endif

# needed to regenerate certdata.c
pushd security/nss/lib/ckfw/builtins
perl ./certdata.perl < /etc/pki/tls/mozilla/certdata.txt
popd

#(tpg) correct the xulrunner version
sed -i -e 's#INTERNAL_VERSION#%{version_internal}#g' xulrunner/installer/Makefile.in

%build
%serverbuild
export PREFIX="%{_prefix}"
export LIBDIR="%{_libdir}"
export CFLAGS="$(echo %{optflags} | sed -e 's/-Wall//')"
export CXXFLAGS="$CFLAGS"
%if %mdkversion >= 200900
export LDFLAGS="%ldflags -Wl,-rpath,%{mozappdir}"
%else
# macro ldflags is nonexisting in older distro versions
export LDFLAGS="$LDFLAGS -Wl,-rpath,%{mozappdir}"
%endif

# (tpg) don't use macro here
# (fhimpe) Starting from Firefox 3.0.1, at least sqlite 3.5.9 is needed
# so don't use system sqlite on Mandriva older than 2009.0
./configure \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--includedir=%{_includedir} \
	--datadir=%{_datadir} \
	--sysconfdir=%{_sysconfdir} \
	--enable-application=xulrunner \
	--with-pthreads \
	--with-system-jpeg \
	--with-system-zlib \
	--with-system-bz2 \
%if %mdkversion >= 200900
	--enable-system-png \
%else
	--disable-system-png \
%endif
	--with-system-nspr \
	--without-system-nss \
%if %mdkversion >= 200800
	--enable-system-sqlite \
%else
	--disable-system-sqlite \
%endif
%if %mdkversion >= 201000
	--enable-system-cairo \
%else
	--disable-system-cairo \
%endif
%if %_use_syshunspell
	--enable-system-hunspell \
%endif
	--disable-javaxpcom \
	--enable-pango \
	--enable-svg \
	--enable-canvas \
	--enable-crypto \
	--disable-crashreporter \
	--disable-installer \
	--disable-updater \
	--enable-optimize="-O2" \
	--enable-jemalloc \
	--disable-wrap-malloc \
	--enable-valgrind \
	--disable-strip \
	--enable-install-strip \
	--enable-startup-notification \
	--enable-default-toolkit=cairo-gtk2 \
	--with-java-include-path=%{java_home}/include \
	--with-java-bin-path=%{java_home}/bin \
	--enable-image-encoder=all \
	--enable-image-decoders=all \
	--enable-places \
	--enable-storage \
	--disable-safe-browsing \
	--enable-url-classifier \
	--enable-gnomevfs \
	--enable-gnomeui \
	--disable-faststart \
	--enable-smil \
	--disable-tree-freetype \
	--enable-canvas3d \
	--disable-coretext \
	--enable-extensions=default \
	--enable-necko-protocols=all \
	--disable-necko-wifi \
	--disable-tests \
	--disable-mochitest \
	--enable-xtf \
	--enable-wave \
	--enable-webm \
	--enable-ogg \
	--enable-xpcom-fastload \
	--enable-gio \
	--enable-dbus \
	--with-distribution-id=com.mandriva

%__perl -p -i -e 's|\-0|\-9|g' config/make-jars.pl

# (tpg) on x86_64 fails when parallel compiling is on
# java.lang.OutOfMemoryError
# since 3.6 it does not
%make

%install
rm -rf %{buildroot}

%makeinstall_std

#install -p dist/sdk/bin/regxpcom %{buildroot}%{mozappdir}

rm -rf %{buildroot}%{_libdir}/%{name}-devel-%{version_internal}/sdk/lib/*.so
pushd %{buildroot}%{mozappdir}
for i in *.so; do
    ln -s %{mozappdir}/$i %{buildroot}%{_libdir}/%{name}-devel-%{version_internal}/sdk/lib/$i
done
popd

# GRE stuff
%ifarch x86_64 ia64 ppc64 s390x
%define gre_conf_file %{version_internal}-64.system.conf
mv %{buildroot}%{_sysconfdir}/gre.d/*.system.conf %{buildroot}%{_sysconfdir}/gre.d/%{gre_conf_file}
%else
%define gre_conf_file %{version_internal}.system.conf
%endif

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

%find_lang %{name}

mkdir -p %{buildroot}%{_sys_macros_dir}
cat <<FIN >%{buildroot}%{_sys_macros_dir}/%{name}.macros
# Macros from %{name} package
%%xulrunner_major            %{major}
%%xulrunner_version          %{version}
%%xulrunner_libname          %{libname}
%%xulrunner_mozappdir        %{mozappdir}
FIN

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENSE README.txt
%dir %{mozappdir}
%{_bindir}/xulrunner

%files -n %{libname}
%defattr(-,root,root)
%{mozappdir}/chrome
%{mozappdir}/dictionaries
%dir %{mozappdir}/components
%ghost %{mozappdir}/components/compreg.dat
%ghost %{mozappdir}/components/xpti.dat
%{mozappdir}/components/*.so
%{mozappdir}/components/*.xpt
%{mozappdir}/components/*.manifest
%attr(644, root, root) %{mozappdir}/components/*.js
%{mozappdir}/defaults
#%{mozappdir}/greprefs
%dir %{mozappdir}/icons
%attr(644, root, root) %{mozappdir}/icons/*
%{mozappdir}/modules
%{mozappdir}/plugins
%{mozappdir}/res
%{mozappdir}/*.so
%{mozappdir}/mozilla-xremote-client
%{mozappdir}/run-mozilla.sh
#%{mozappdir}/regxpcom
%{mozappdir}greprefs.js
%{mozappdir}/*.chk
%{mozappdir}/xulrunner
%{mozappdir}/xulrunner-bin
%{mozappdir}/xulrunner-stub
%{mozappdir}/platform.ini
%{mozappdir}/dependentlibs.list
#%{mozappdir}/javaxpcom.jar
%{mozappdir}/plugin-container
%dir %{_sysconfdir}/gre.d
%{_sysconfdir}/gre.d/*.conf

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/%{name}-%{version_internal}
%{mozappdir}/xpcshell
%{mozappdir}/xpidl
%{mozappdir}/xpt_dump
%{mozappdir}/xpt_link
%{_libdir}/%{name}-devel-%{version_internal}
%{_libdir}/pkgconfig/*.pc
%{_datadir}/idl/%{name}-%{version_internal}
%{_sys_macros_dir}/%{name}.macros
