Name:          8188eu-kmod
Version:       4.3.0.7_12758.20141114
Release:       3%{?dist}
Summary:       Realtek RTL8188EUS Linux Driver
URL:           http://www.realtek.com.tw/products
Group:         System Environment/Kernel 
License:       GPLv2

Source0:       rtl8188EUS_linux_v%{version}.tar.gz

Patch000:      8188eu-kmod-ignore-gcc-date-time-warning.patch
Patch001:      8188eu-kmod-better-gcc-optimization.patch

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
%patch000 -p1 -b .ignore-gcc-date-time-warning
%patch001 -p1 -b .better-gcc-optimization
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
* Sun Mar 22 2015 Marcelo 'codeN' Gonzalez <koaeH@aol.com> - 4.3.0.7-3
- Rebuild for kernel 3.19.1-201.fc21
- Migrate back to RPM Fusion

* Fri Feb 20 2015 Marcelo 'codeN' Gonzalez <koaeH@aol.com> - 4.3.0.7-2
- Rebuild for kernel 3.18.7-200.fc21

* Sun Feb 08 2015 Marcelo 'codeN' Gonzalez <koaeH@aol.com> - 4.3.0.7-1
- Migrate from RPM Fusion to LABNET Repository

* Thu Feb 05 2015 Marcelo 'codeN' Gonzalez <koaeH@aol.com> - 4.3.0.7-0
- Update to RTL8188EUS_linux_v4.3.0.7_12758.20141114.tar.gz
