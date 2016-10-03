Name:          8188eu-kmod
Version:       4.3.0.8_13968.20150417
Release:       22%{?dist}
Summary:       Realtek RTL8188EUS Linux Driver
URL:           http://www.realtek.com.tw/products
Group:         System Environment/Kernel 
License:       GPLv2

Source0:       rtl8188EUS_linux_v%{version}.tar.gz

Patch000:      8188eu-kmod-better-gcc-optimization.patch
Patch001:      8188eu-kmod-ignore-gcc-date-time-warning.patch
Patch002:      8188eu-kmod-ignore-gcc-implicit-func-decl.patch
Patch003:      8188eu-kmod-strnicmp-2-strncasecmp-bugfix.patch
Patch004:      8188eu-kmod-rename-used-var-phy_file_path.patch
Patch005:      8188eu-kmod-seqdump-missing-return-value.patch
Patch006:      8188eu-kmod-replace-is_compat_task.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: %{_bindir}/kmodtool
ExclusiveArch: i686 x86_64 %{arm}

%global buildforkernels newest
%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu}}
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null)}

%description
This package provides Realtek's RTL8188EUS single-chip IEEE 802.11b/g/n WLAN 
controller with USB2.0 interface linux driver. Common wireless USB adapters
containing this chip are TL-WN725N, CF-WU712P and RT5370. This is not the
same driver as the one from the linux kernel staging area.

%prep
%{?kmodtool_check}
kmodtool \
  --target %{_target_cpu} \
  --repo rpmfusion --kmodname %{name} \
  %{?buildforkernels:--%{buildforkernels}} \
  %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c -T
tar xf %{SOURCE0}
pushd rtl8188EUS_linux_v%{version}
%patch000 -p1 -b .better-gcc-optimization
%patch001 -p1 -b .ignore-gcc-date-time-warning
%patch002 -p1 -b .ignore-gcc-implicit-func-decl
%patch003 -p1 -b .strnicmp-2-strncasecmp-bugfix
%patch004 -p1 -b .rename-used-var-phy_file_path
%patch005 -p1 -b .seqdump-missing-return-value
%patch006 -p1 -b .replace-is_compat_task
popd

for kernel_version in %{?kernel_versions}; do
  cp -a rtl8188EUS_linux_v%{version} _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version in %{?kernel_versions}; do
 pushd _kmod_build_${kernel_version%%___*}
 make KSRC="${kernel_version##*___}"
 popd
done

%install
rm -rf ${RPM_BUILD_ROOT}
for kernel_version in %{?kernel_versions}; do
  pushd _kmod_build_${kernel_version%%___*}
  sed -r -i.ko-mode-0755 '/^\s+install/s/0*644/0755/' -- Makefile
  sed -r -i.no-depmod-execution '\#^\s+/sbin/depmod\s+-a#d' -- Makefile
  mkdir -p -m 755 $RPM_BUILD_ROOT/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
  make MODDESTDIR=$RPM_BUILD_ROOT/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix} install
  popd
done

%{?akmod_install}

%clean
rm -r -f $RPM_BUILD_ROOT

%changelog
* Sat Oct 01 2016 Marcelo 'codeN' Gonzalez <koaeH@aol.com> - 4.3.0.8-22
- Rebuild for kernel-4.7.4-100.fc23

* Mon Aug 01 2016 Marcelo 'codeN' Gonzalez <koaeH@aol.com> - 4.3.0.8-21
- Rebuild for kernel-4.6.4-201.fc23
- Patch s/is_compat_task/in_compat_syscall/ @os_dep/linux/rtw_android.c

* Sun May 08 2016 Marcelo 'codeN' Gonzalez <koaeH@aol.com> - 4.3.0.8-20
- Rebuild for kernel-4.4.8-300.fc23

* Thu Mar 24 2016 Marcelo 'codeN' Gonzalez <koaeH@aol.com> - 4.3.0.8-19
- Rebuild for kernel-4.4.6-300.fc23

* Sun Mar 20 2016 Marcelo 'codeN' Gonzalez <koaeH@aol.com> - 4.3.0.8-18
- Rebuild for kernel-4.4.5-300.fc23

* Wed Mar 09 2016 Marcelo 'codeN' Gonzalez <koaeH@aol.com> - 4.3.0.8-17
- Rebuild for kernel-4.4.3-300.fc23

* Wed Mar 02 2016 Marcelo 'codeN' Gonzalez <koaeH@aol.com> - 4.3.0.8-16
- Rebuild for kernel 4.4.2-301.fc23

* Fri Feb 19 2016 Marcelo 'codeN' Gonzalez <koaeH@aol.com> - 4.3.0.8-15
- Rebuild for kernel 4.3.5-300.fc23

* Wed Feb 10 2016 Marcelo 'codeN' Gonzalez <koaeH@aol.com> - 4.3.0.8-14
- Rebuild for kernel 4.3.4-300.fc23

* Fri Jan 29 2016 Marcelo 'codeN' Gonzalez <koaeH@aol.com> - 4.3.0.8-12
- Rebuild for kernel 4.3.3-301.fc23

* Sun Jan 24 2016 Marcelo 'codeN' Gonzalez <koaeH@aol.com> - 4.3.0.8-11
- Patch missing return value of _seqdump (workaround @rtw_debug.h)

* Thu Jan 14 2016 Marcelo 'codeN' Gonzalez <koaeH@aol.com> - 4.3.0.8-10
- Rebuild for kernel 4.3.3-300.fc23

* Mon Dec 28 2015 Marcelo 'codeN' Gonzalez <koaeH@aol.com> - 4.3.0.8-9
- Rebuild for kernel 4.2.8-300.fc23

* Sun Dec 20 2015 Marcelo 'codeN' Gonzalez <koaeH@aol.com> - 4.3.0.8-8
- Rebuild for kernel 4.2.7-300.fc23

* Tue Dec 01 2015 Marcelo 'codeN' Gonzalez <koaeH@aol.com> - 4.3.0.8-7
- Rebuild for kernel 4.2.6-301.fc23

* Mon Nov 30 2015 Marcelo 'codeN' Gonzalez <koaeH@aol.com> - 4.3.0.8-6
- Rebuild for kernel 4.2.6-200.fc22
- Patch s/file_path/phy_file_path/ @hal/hal_com_phycfg.c

* Thu Aug 20 2015 Marcelo 'codeN' Gonzalez <koaeH@aol.com> - 4.3.0.8-5
- Rebuild for kernel 4.1.5-200.fc22

* Sun Aug 16 2015 Marcelo 'codeN' Gonzalez <koaeH@aol.com> - 4.3.0.8-4
- Patch s/strnicmp/strncasecmp/ @os_dep/linux/rtw_android.c

* Wed Aug 12 2015 Marcelo 'codeN' Gonzalez <koaeH@aol.com> - 4.3.0.8-3
- Rebuild for kernel 4.1.4-200.fc22

* Mon Jul 13 2015 Marcelo 'codeN' Gonzalez <koaeH@aol.com> - 4.3.0.8-2
- Rebuild for kernel 4.0.7-300.fc22

* Sun Jun 21 2015 Marcelo 'codeN' Gonzalez <koaeH@aol.com> - 4.3.0.8-1
- Rebuild for kernel 4.0.5-300.fc22

* Thu Jun 11 2015 Marcelo 'codeN' Gonzalez <koaeH@aol.com> - 4.3.0.8-0
- Update to RTL8188EUS_linux_v4.3.0.8_13968.20150417
- Rebuild for kernel 4.0.4-202.fc21

* Wed May 13 2015 Marcelo 'codeN' Gonzalez <koaeH@aol.com> - 4.3.0.7-4
- Rebuild for kernel 3.19.5-200.fc21

* Sun Mar 22 2015 Marcelo 'codeN' Gonzalez <koaeH@aol.com> - 4.3.0.7-3
- Rebuild for kernel 3.19.1-201.fc21
- Migrate back to RPM Fusion

* Fri Feb 20 2015 Marcelo 'codeN' Gonzalez <koaeH@aol.com> - 4.3.0.7-2
- Rebuild for kernel 3.18.7-200.fc21

* Sun Feb 08 2015 Marcelo 'codeN' Gonzalez <koaeH@aol.com> - 4.3.0.7-1
- Migrate from RPM Fusion to LABNET Repository

* Thu Feb 05 2015 Marcelo 'codeN' Gonzalez <koaeH@aol.com> - 4.3.0.7-0
- Update to RTL8188EUS_linux_v4.3.0.7_12758.20141114.tar.gz
