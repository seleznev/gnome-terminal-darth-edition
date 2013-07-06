%define gettext_package gnome-terminal

%define glib2_version 2.33.0
%define gtk3_version 3.6.0
%define vte_version 0.34.0
%define desktop_file_utils_version 0.2.90

Summary: Terminal emulator for GNOME, Darth edition
Name: gnome-terminal-darth-edition
Version: 3.8.2
Release: 1%{?dist}
License: GPLv3+ and GFDL
Group: User Interface/Desktops
URL: http://www.gnome.org/
#VCS: git:git://git.gnome.org/gnome-terminal
Source0: http://download.gnome.org/sources/gnome-terminal/3.8/gnome-terminal-%{version}.tar.xz
Patch: gnome-terminal-3.8.2-darth-edition.patch

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

Requires: gsettings-desktop-schemas

Conflicts: gnome-terminal
Obsoletes: gnome-terminal
Provides: gnome-terminal

%description
gnome-terminal is a terminal emulator for GNOME. It features the ability to use
multiple terminals in a single window (tabs) and profiles support.

%prep
%setup -q -n gnome-terminal-%{version}
%patch -p1 -b .darth-edition

%build
%configure --with-gtk=3.0

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-install --vendor gnome --delete-original	\
  --dir $RPM_BUILD_ROOT%{_datadir}/applications		\
  --remove-category=Application				\
  --add-category=System					\
  $RPM_BUILD_ROOT%{_datadir}/applications/gnome-terminal.desktop

%find_lang %{gettext_package} --with-gnome

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

%changelog
* Sun Jul 7 2013 Alexander Seleznev <SeleznevRU@gmail.com> - 3.8.2-1
- Update to 3.8.2