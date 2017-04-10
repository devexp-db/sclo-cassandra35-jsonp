%{?scl:%scl_package jsonp}
%{!?scl:%global pkg_name %{name}}

%global namedreltag %{nil}
%global namedversion %{version}%{?namedreltag}

Name:		%{?scl_prefix}jsonp
Version:	1.0.4
Release:	6%{?dist}
Summary:	JSR 353 (JSON Processing) RI
License:	CDDL or GPLv2 with exceptions
URL:		http://java.net/projects/jsonp/
# git clone git://java.net/jsonp~git jsonp
# (cd jsonp/ && git archive --format=tar --prefix=jsonp-1.0.4/ jsonp-1.0.4 | xz > ../jsonp-1.0.4.tar.xz)
Source0:	%{pkg_name}-%{namedversion}.tar.xz
# wget -O glassfish-LICENSE.txt https://svn.java.net/svn/glassfish~svn/tags/legal-1.1/src/main/resources/META-INF/LICENSE.txt
# jsonp package don't include the license file
Source1:	glassfish-LICENSE.txt

BuildRequires:	%{?scl_prefix_maven}jvnet-parent
BuildRequires:	%{?scl_prefix}glassfish-jax-rs-api >= 2.0-2
# test deps
BuildRequires:	%{?scl_prefix_java_common}junit
BuildRequires:	%{?scl_prefix_maven}maven-local
BuildRequires:	%{?scl_prefix_maven}maven-plugin-bundle
BuildRequires:	%{?scl_prefix_maven}spec-version-maven-plugin
%{?scl:Requires: %scl_runtime}
BuildArch:	noarch

%description
JSR 353: Java API for Processing JSON RI.

%package javadoc
Summary:	Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{pkg_name}-%{namedversion}
find . -name '*.jar' -delete
find . -name '*.class' -delete

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
# Unwanted old apis
%pom_disable_module bundles
%pom_disable_module demos
%pom_disable_module gf
%pom_disable_module tests

%pom_remove_dep javax:javaee-web-api

%pom_remove_plugin org.glassfish.copyright:glassfish-copyright-maven-plugin
%pom_remove_plugin org.codehaus.mojo:wagon-maven-plugin
%pom_remove_plugin org.apache.maven.plugins:maven-dependency-plugin impl

# disabled source and javadoc jars
%pom_remove_plugin org.apache.maven.plugins:maven-source-plugin
%pom_remove_plugin :maven-source-plugin api
%pom_remove_plugin :maven-javadoc-plugin api
%pom_remove_plugin :maven-jar-plugin impl
%pom_remove_plugin :maven-javadoc-plugin impl
%pom_remove_plugin :maven-source-plugin impl
%pom_remove_plugin :maven-javadoc-plugin jaxrs

sed -i '/check-module/d' api/pom.xml impl/pom.xml

# disable apis copy
%pom_xpath_remove "pom:build/pom:plugins/pom:plugin[pom:artifactId ='maven-bundle-plugin']/pom:configuration/pom:instructions/pom:Export-Package"  impl

cp -p %{SOURCE1} LICENSE.txt
sed -i 's/\r//' LICENSE.txt

%pom_xpath_set "pom:parent/pom:version" %{namedversion} api
%pom_xpath_set "pom:parent/pom:version" %{namedversion} jaxrs

%mvn_file :javax.json-api %{pkg_name}/%{pkg_name}-api
%mvn_file :javax.json %{pkg_name}/%{pkg_name}
%mvn_file :%{pkg_name}-jaxrs %{pkg_name}/%{pkg_name}-jaxrs
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_build
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%license LICENSE.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Mon Apr 10 2017 Tomas Repik <trepik@redhat.com> - 1.0.4-6
- scl conversion

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Feb 09 2015 gil cattaneo <puntogil@libero.it> 1.0.4-2
- introduce license macro

* Tue Nov 18 2014 gil cattaneo <puntogil@libero.it> 1.0.4-1
- update to 1.0.4

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.0-5
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 09 2013 gil cattaneo <puntogil@libero.it> 1.0-3
- switch to XMvn
- minor changes to adapt to current guideline

* Sun May 26 2013 gil cattaneo <puntogil@libero.it> 1.0-2
- rebuilt with spec-version-maven-plugin support

* Tue May 07 2013 gil cattaneo <puntogil@libero.it> 1.0-1
- update to 1.0

* Tue Mar 26 2013 gil cattaneo <puntogil@libero.it> 1.0-0.1.b06
- initial rpm
