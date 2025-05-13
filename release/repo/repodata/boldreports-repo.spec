Summary: Bold Reports YUM repository configuration
Name: boldreports-repo
Version: 1.1
Release: 1
License: GPL
Group: System/Packages
BuildArch: noarch
Source0: boldreports.repo

%description
This package installs the Bold Reports repository configuration file in /etc/yum.repos.d/.

%prep

%build

%install
mkdir -p %{buildroot}/etc/yum.repos.d/
cp %{SOURCE0} %{buildroot}/etc/yum.repos.d/boldreports.repo

%files
/etc/yum.repos.d/boldreports.repo

%changelog