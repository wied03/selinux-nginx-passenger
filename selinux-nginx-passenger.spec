Summary:	SELinux module for NGinx+Passenger
Name:		selinux-nginx-passenger
Version:	0.1
Release:	0.1%{?dist}
License:        Public Domain
Requires:   policycoreutils >= 2.2.5
BuildRequires:	policycoreutils-python >= 2.2.5, selinux-policy-devel >= 3.12.1
Source0:	nginx-passenger.fc
Source1:	nginx-passenger.te

%description
SELinux/NGinx Passenger stuff

%prep
cp -p %SOURCE0 %SOURCE1 .
find .

%build
make -f %{_datadir}/selinux/devel/Makefile

%install
install -p -m 644 -D nginx-passenger.pp $RPM_BUILD_ROOT%{_datadir}/selinux/packages/%{name}/nginx-passenger.pp

%clean
make -f %{_datadir}/selinux/devel/Makefile clean

%files
%{_datadir}/selinux/packages/%{name}/nginx-passenger.pp

%post
if [ "$1" -le "1" ] ; then # First install
semodule -i %{_datadir}/selinux/packages/%{name}/nginx-passenger.pp 2>/dev/null || :
fixfiles -R nginx restore
fixfiles -R passenger restore
/bin/systemctl restart nginx > /dev/null 2>&1 || :
fi

%preun
if [ "$1" -lt "1" ] ; then # Final removal
semodule -r nginx-passenger 2>/dev/null || :
fixfiles -R nginx restore
fixfiles -R passenger restore
/bin/systemctl restart nginx > /dev/null 2>&1 || :
fi

%postun
if [ "$1" -ge "1" ] ; then # Upgrade
semodule -i %{_datadir}/selinux/packages/%{name}/nginx-passenger.pp 2>/dev/null || :
fi
