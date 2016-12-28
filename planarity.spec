Name:		planarity
Summary:	Implementations of several planarity-related graph algorithms
Version:	2.2.0
Release:	1
Group:		Development/C
License:	BSD
URL:		https://code.google.com/p/%{name}/
Source0:	http://mirrors.mit.edu/sage/spkg/upstream/%{name}/%{name}-%{version}.tar.bz2
Source1:	SPKG.txt
# Edited output of help2man
Source2:	%{name}.1
# sagemath patches renamed with planarity- prefix
Patch0:		%{name}-extern.patch
Patch1:		%{name}-without_nauty.patch
Patch2:		%{name}-malloc.patch

%description
This code project provides a library for implementing graph algorithms
as well as implementations of several planarity-related graph algorithms.
The origin of this project is the reference implementation for the Edge
Addition Planarity Algorithm, which is now the fastest and simplest
linear-time method for planar graph embedding and planarity obstruction
isolation (i.e. Kuratowski subgraph isolation).

The software in this code project provides a graph algorithm framework and
library, including an updated version of the edge addition combinatorial
planar graph embedder and planar obstruction isolator (i.e., a Kuratowski
subgraph isolator). This code project also includes several extensions
that implement planarity-related algorithms such as a planar graph drawing
algorithm, an outerplanar graph embedder and outerplanar obstruction
isolator, and a number of subgraph homeomorphism search algorithms.

%package	devel
Summary:	Development files for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{_lib}planarity0 = %{version}-%{release}

%description	devel
This package contains the header files and development documentation
for %{name}.

%libpackage planarity 0
%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

# Use unix line endings in installed headers
for header in c/*.h; do
    sed -e 's|\r$||g' $header > $header.tmp
    # Preserve timestamps
    touch -r $header $header.tmp
done

%build
%configure --enable-static=false

# Get rid of undesirable hardcoded rpaths
sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    -i libtool

# Do not use hardcoded CFLAGS=-O3
make %{?_smp_mflags} CFLAGS="%{optflags}"

%install
make install DESTDIR="%{buildroot}"
rm %{buildroot}%{_libdir}/*.la
install -p -m644 -D %{SOURCE1} %{buildroot}%{_docdir}/%{name}/SPKG.txt
install -p -m644 -D %{SOURCE2} %{buildroot}%{_mandir}/man1/%{name}.1

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING
%doc %{_mandir}/man1/%{name}.1*
%{_bindir}/%{name}

%files	devel
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so

%changelog
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov  4 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.2.0-1
- Initial planarity spec.
