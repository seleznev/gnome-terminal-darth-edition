%define gettext_package gnome-terminal

%define glib2_version 2.33.2
%define gtk3_version 3.9.9
%define vte_version 0.34.7
%define desktop_file_utils_version 0.2.90

Summary: Terminal emulator for GNOME, Darth edition
Name: gnome-terminal-darth-edition
Version: 3.10.2
Release: 1%{?dist}
License: GPLv3+ and GFDL
Group: User Interface/Desktops
URL: http://www.gnome.org/
#VCS: git:git://git.gnome.org/gnome-terminal
Source0: http://download.gnome.org/sources/gnome-terminal/3.10/gnome-terminal-%{version}.tar.xz
Patch: gnome-terminal-%{version}-darth-edition.patch

BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: GConf2-devel
BuildRequires: gtk3-devel >= %{gtk3_version}
BuildRequires: gsettings-desktop-schemas-devel
BuildRequires: vte3-devel >= %{vte_version}
BuildRequires: desktop-file-utils >= %{desktop_file_utils_version}
BuildRequires: gettext
BuildRequires: intltool
BuildRequires: gnome-common
BuildRequires: autoconf automake libtool
BuildRequires: itstool
BuildRequires: dconf-devel
BuildRequires: libuuid-devel
BuildRequires: nautilus-devel

Requires: gsettings-desktop-schemas
Requires: vte3%{?_isa} >= %{vte_version}

Conflicts: gnome-terminal
Obsoletes: gnome-terminal
Provides: gnome-terminal

%description
gnome-terminal is a terminal emulator for GNOME. It features the ability to use
multiple terminals in a single window (tabs) and profiles support.

%package nautilus
Summary: GNOME Terminal extension for Nautilus
Requires: %{name}%{?_isa} = %{version}-%{release}

%description nautilus
This package provides a Nautilus extension that adds the 'Open in Terminal'
option to the right-click context menu in Nautilus.

%prep
%setup -q -n gnome-terminal-%{version}
%patch -p1 -b .darth-edition

%build
%configure --disable-static --with-gtk=3.0 --with-nautilus-extension

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-3.0/*.la

%find_lang %{gettext_package} --with-gnome

%check
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/gnome-terminal.desktop

%postun
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files -f %{gettext_package}.lang
%doc AUTHORS COPYING NEWS

%{_bindir}/gnome-terminal
%{_datadir}/applications/gnome-terminal.desktop
%{_libexecdir}/gnome-terminal-migration
%{_libexecdir}/gnome-terminal-server
%{_datadir}/dbus-1/services/org.gnome.Terminal.service
%{_datadir}/glib-2.0/schemas/org.gnome.Terminal.gschema.xml

%files nautilus
%{_libdir}/nautilus/extensions-3.0/libterminal-nautilus.so

%changelog
* Sun Dec 8 2013 Alexander Seleznev <SeleznevRU@gmail.com> - 3.10.2-1
- Rebase on 3.10.2

* Mon Aug 5 2013 Alexander Seleznev <SeleznevRU@gmail.com> - 3.8.4-1
- Update to 3.8.4

* Sun Jul 7 2013 Alexander Seleznev <SeleznevRU@gmail.com> - 3.8.2-1
- Update to 3.8.2
