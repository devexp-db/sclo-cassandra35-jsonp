%global namedreltag %{nil}
%global namedversion %{version}%{?namedreltag}
Name:          jsonp
Version:       1.0
Release:       3%{?dist}
Summary:       JSR 353 (JSON Processing) RI
License:       CDDL or GPLv2 with exceptions
URL:           http://java.net/projects/jsonp/
# git clone git://java.net/jsonp~git jsonp
# (cd jsonp/ && git archive --format=tar --prefix=jsonp-1.0/ json-1.0 | xz > ../jsonp-1.0-src-git.tar.xz)
Source0:       %{name}-%{namedversion}-src-git.tar.xz
# wget -O glassfish-LICENSE.txt https://svn.java.net/svn/glassfish~svn/tags/legal-1.1/src/main/resources/META-INF/LICENSE.txt
# jsonp package don't include the license file
Source1:       glassfish-LICENSE.txt

BuildRequires: java-devel
BuildRequires: jvnet-parent

BuildRequires: glassfish-jax-rs-api >= 2.0-2

#test deps
BuildRequires: junit

BuildRequires: maven-local
BuildRequires: maven-plugin-bundle
#BuildRequires: maven-surefire-provider-junit4
BuildRequires: spec-version-maven-plugin

BuildArch:     noarch

%description
JSR 353: Java API for Processing JSON RI.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-%{namedversion}
find . -name '*.jar' -delete
find . -name '*.class' -delete
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

# disable apis copy
%pom_xpath_remove "pom:build/pom:plugins/pom:plugin[pom:artifactId ='maven-bundle-plugin']/pom:configuration/pom:instructions/pom:Export-Package"  impl

cp -p %{SOURCE1} LICENSE.txt
sed -i 's/\r//' LICENSE.txt

%build

%mvn_file :javax.json-api %{name}/%{name}-api
%mvn_file :javax.json %{name}/%{name}
%mvn_file :%{name}-jaxrs %{name}/%{name}-jaxrs
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Tue Jul 09 2013 gil cattaneo <puntogil@libero.it> 1.0-3
- switch to XMvn
- minor changes to adapt to current guideline

* Sun May 26 2013 gil cattaneo <puntogil@libero.it> 1.0-2
- rebuilt with spec-version-maven-plugin support

* Tue May 07 2013 gil cattaneo <puntogil@libero.it> 1.0-1
- update to 1.0

* Tue Mar 26 2013 gil cattaneo <puntogil@libero.it> 1.0-0.1.b06
- initial rpm