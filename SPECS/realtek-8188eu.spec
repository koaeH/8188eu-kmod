Name:          realtek-8188eu
Version:       4.3.0.8_13968.20150417
Release:       16%{?dist}
Summary:       Common files for Realtek RTL8188EUS Linux Driver
URL:           http://www.realtek.com.tw/products
Group:         System Environment/Kernel 
License:       GPLv2

Source0:       LICENSE

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
ExcludeArch:   ppc 

Provides:      8188eu-kmod-common = %{version}
Requires:      8188eu-kmod >= %{version}
Conflicts:     kmod-staging

%description
This package provides Realtek's RTL8188EUS single-chip IEEE 802.11b/g/n WLAN 
controller with USB2.0 interface linux driver. Common wireless USB adapters
containing this chip are TL-WN725N, CF-WU712P and RT5370. N.B. This is not
the same driver as the one from the linux kernel staging area.

%prep
%setup -q -c -T
%define debug_package %{nil}
install -p -m 0644 %{SOURCE0} .

%build

%install
rm -rf $RPM_BUILD_ROOT

%clean
rm -r -f $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc LICENSE

%changelog
* Thu Jun 11 2015 Marcelo 'codeN' Gonzalez <koaeH@aol.com> - 4.3.0.8-0
- Update to RTL8188EUS_linux_v4.3.0.8_13968.20150417

* Thu Feb 05 2015 Marcelo 'codeN' Gonzalez <koaeH@aol.com> - 4.3.0.7-0
- Update to RTL8188EUS_linux_v4.3.0.7_12758.20141114.tar.gz
