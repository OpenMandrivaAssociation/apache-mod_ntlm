#Module-Specific definitions
%define mod_name mod_ntlm
%define mod_conf 97_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	NTLM authentication module for apache
Name:		apache-%{mod_name}
Version:	0.2
Release:	%mkrel 6
Group:		System/Servers
License:	BSD
URL:		http://modntlm.jamiekerwick.co.uk/
Source0: 	http://modntlm.jamiekerwick.co.uk/ntlm2.tar.bz2
Source1:	%{mod_conf}.bz2
Source2:	README.html.bz2
Patch0:		ntlm2-apr1.diff
Patch1:		ntlm2-gcc4.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file
Epoch:		2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This module is implementing NTLM authentication for apache on
Unix platforms.

%prep

%setup -q -c -n %{mod_name}
%patch0 -p0
%patch1 -p0

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

bzcat %{SOURCE1} > %{mod_conf}
bzcat %{SOURCE2} > README.html

%build

%{_sbindir}/apxs -c %{mod_name}.c


%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -d %{buildroot}%{_var}/www/html/addon-modules
ln -s ../../../..%{_docdir}/%{name}-%{version} %{buildroot}%{_var}/www/html/addon-modules/%{name}-%{version}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README.html
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_var}/www/html/addon-modules/*


