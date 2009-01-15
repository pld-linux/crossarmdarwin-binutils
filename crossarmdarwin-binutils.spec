# DOCS
# - http://aakash-bapna.blogspot.com/2007/10/iphone-non-official-sdk-aka-toolchain.html
# - http://code.google.com/p/iphone-dev/wiki/Building
#  - ...
#  - csu (crt1.o, dylib1.o, and bundle1.o) + bootstrap
#  - ...
# TO MAKE TARBALL(s):
# svn co http://iphone-dev.googlecode.com/svn/trunk/odcctools odcctools
# tar --exclude=.svn -cjf odcctools-r280.tar.bz2 odcctools
# TODO
# - name of this cross platform? crossarm-darwin? crossarm-darwin9?
# - not built from binutils source, should we name package differently?
# - On 64-bit architectures there are currently compilation and linking problems with structs and typedefs; as a workaround, try the following:
# - export CFLAGS="-m32"; export LDFLAGS="-m32"
Summary:	Cross ARM Apple Darwin development utilities - binutils
Name:		crossarmdarwin-binutils
Version:	0.152
Release:	0.1
License:	GPL v2
Group:		Development/Tools
Source0:	odcctools-r280.tar.bz2
# Source0-md5:	8a49b63a883219705de5b4a95265ffca
URL:		http://developer.berlios.de/projects/iphone-binutils/
BuildRequires:	bison
BuildRequires:	flex
%ifarch %{x8664}
# SILLY! there should had been %{target_base_arch} if any at all
BuildRequires:	glibc-devel(athlon)
BuildRequires:	gcc-multilib
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		arm-apple-darwin
%define		arch		%{_prefix}/%{target}

%description
Binutils is a collection of binary utilities, including:
- ar - create, modify and extract from archives,
- nm - lists symbols from object files,
- objcopy - copy and translate object files,
- objdump - display information from object files,
- ranlib - generate an index for the contents of an archive,
- size - list the section sizes of an object or archive file,
- strings - list printable strings from files,
- strip - discard symbols,
- c++filt - a filter for demangling encoded C++ symbols,
- addr2line - convert addresses to file and line,
- nlmconv - convert object code into an NLM.

This is a toolchain to produce arm/Mach-O binaries.

%description -l pl.UTF-8
Pakiet binutils zawiera zestaw narzędzi umożliwiających kompilację
programów. Znajdują się tutaj między innymi assembler, konsolidator
(linker), a także inne narzędzia do manipulowania binarnymi plikami
programów i bibliotek.

%prep
%setup -qcT -a0

%build
install -d build/odcctools
cd build/odcctools
../../odcctools/%configure \
%ifarch %{x8664}
	CFLAGS="%{rpmcflags} -m32" \
	LDFLAGS="%{rpmldflags} -m32" \
%endif
	--prefix=%{arch} \
	--libexecdir=%{arch} \
	--target=%{target} \
	--disable-ld64
%{__make}
cd -

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_prefix}

%{__make} -C build/odcctools install \
	DESTDIR=$RPM_BUILD_ROOT

# prefix manpages
for a in $RPM_BUILD_ROOT%{_mandir}/man?/*; do
	n=${a##*/} s=${a##*.} d=${a%/*}
	mv $a $d/%{target}-$n.$s
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-*
%dir %{arch}
%dir %{arch}/as
%dir %{arch}/as/*
%attr(755,root,root) %{arch}/as/*/as

%{_mandir}/man?/%{target}-*
%dir %{_includedir}/mach-o
%{_includedir}/mach-o/arch.h
%{_includedir}/mach-o/fat.h
%{_includedir}/mach-o/loader.h
%{_includedir}/mach-o/machine.h
%{_libdir}/libmacho.a
