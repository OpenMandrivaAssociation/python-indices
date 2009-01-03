%define oname   indices
%define name    python-%oname
%define version 0.1
%define release %mkrel 8


Summary:       Sequence index, item ranges, and enumeration for python
Name:          %{name}
Version:       %{version}
Release:       %{release}
Source0:       %{oname}.py
License:       LGPL
Group:         Development/Python
BuildRoot:     %{_tmppath}/%{name}-buildroot
Url:           http://www.python.org/peps/pep-0212.html
BuildRequires: python

%description
This is a python module providing a number of functions to make it
easier to iterate over sequences, based on PEP 212 and PEP 279.

%install
rm -rf $RPM_BUILD_ROOT
install -m644 -D %SOURCE0 $RPM_BUILD_ROOT/%{_libdir}/python%pyver/site-packages/%{oname}.py
cd $RPM_BUILD_ROOT/%{_libdir}/python%pyver/site-packages/
python -c "import %{oname}"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_libdir}/python%pyver/site-packages/%{oname}.py*

