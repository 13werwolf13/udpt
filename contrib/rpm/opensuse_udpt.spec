#
# spec file for package udpt
#
# Copyright (c) 2024 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


Name:           udpt
Version:        3.1.2
Release:        0
Summary:        A lightweight UDP torrent tracker
License:        MIT
URL:            https://github.com/naim94a/udpt
Source0:        udpt-3.1.2.tar.zst
Source2:        vendor.tar.zst
Source1:        contrib.tar.zst
BuildRequires:  cargo-packaging
BuildRequires:  systemd-rpm-macros
BuildRequires:  sysuser-tools
BuildRequires:  zstd
Provides:       user(udpt)
%{sysusers_requires}

%description
UDPT is a lightweight torrent tracker that uses the UDP protocol for tracking and fully implements BEP-15. This project was developed with security & simplicity in mind, so it shouldn't be difficult to get a server started.

%prep
%autosetup -a1 -a2 -a3

%build
%{cargo_build}

%install
install -Dm 755  target/release/udpt-rs %{buildroot}%{_bindir}/udpt
install -Dm 644  contrib/systemd/udpt.service %{buildroot}%{_unitdir}/udpt.service
install -Dm 644  contrib/systemd/udpt.tmpfiles %{buildroot}%{_tmpfilesdir}/udpt.conf
install -Dm 644  contrib/systemd/udpt.sysusers %{buildroot}%{_sysusersdir}/system-user-udpt.conf
install -Dm 644  contrib/systemd/udpt.conf %{buildroot}%{_sysconfdir}/udpt.conf

%files
%license LICENSE
%doc README.md
%{_bindir}/udpt
%{_unitdir}/udpt.service
%{_tmpfilesdir}/udpt.conf
%{_sysusersdir}/system-user-udpt.conf

%pre -f udpt.pre
%service_add_pre udpt.service

%post
%sysusers_create %{_sysusersdir}/system-user-udpt.conf
%tmpfiles_create %{_tmpfilesdir}/udpt.conf
%service_add_post udpt.service

%preun
%service_del_preun udpt.service

%postun
%service_del_postun udpt.service

%changelog

