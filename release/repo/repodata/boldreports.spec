Name:           boldreports
Version:        9.l.7
Release:        1%{?dist}
Summary:        Bold Reports Enterprise Reporting Package

License:        Proprietary
URL:            https://www.boldreports.com/
BuildArch:      noarch
Requires:       zip, wget, nginx, unzip, bash, libicu, libgdiplus, python3-pip, pv, nss(x86-64), libdrm, mesa-libgbm, libxshmfence, pango(x86-64), libXcomposite(x86-64), libXcursor(x86-64), libXdamage(x86-64), libXext(x86-64), libXi(x86-64), libXtst(x86-64), cups-libs(x86-64), libXScrnSaver(x86-64), libXrandr(x86-64), alsa-lib(x86-64), atk(x86-64), gtk3(x86-64), xorg-x11-fonts-100dpi, xorg-x11-fonts-75dpi, xorg-x11-utils, xorg-x11-fonts-cyrillic, xorg-x11-fonts-Type1, xorg-x11-fonts-misc
Requires(pre):  unzip
Requires(post): bash

Source0:        boldreports-package.zip

%description
This package installs and configures Bold Reports Enterprise Reporting Application with necessary dependencies and options for installation type, user, and front-end configuration.

%global __strip /bin/true

%prep
# Unzip the source files to the build directory
mkdir -p %{_builddir}/boldreports
unzip -o %{SOURCE0} -d %{_builddir}/boldreports

%build
# No build commands required as this is a script-based package

%install
# Copy application files to the target directory
mkdir -p %{buildroot}/opt/boldreports
cp -R %{_builddir}/boldreports/* %{buildroot}/opt/boldreports/

%files
/opt/boldreports/*

%post
echo "Post-installation script started."

# Check if /var/www/bold-services exists
if [ -d "/var/www/bold-services" ]; then
    echo "Directory /var/www/bold-services exists."
    i=1  # Flag to indicate the folder exists
else
    echo "Directory /var/www/bold-services does not exist."
    i=0
fi

# If the folder exists, extract the Idp URL from product.json and run the installation script
if [ "$i" -eq 1 ]; then
    CONFIG_FILE="/var/www/bold-services/application/app_data/configuration/product.json"
    if [ -f "$CONFIG_FILE" ]; then
        echo "Configuration file found: $CONFIG_FILE"
        IDP_URL=$(grep '"Idp"' "$CONFIG_FILE" | sed -E 's/.*"Idp": ?"([^"]+)".*/\1/')
        if [ -n "$IDP_URL" ]; then
            echo "Idp URL: $IDP_URL"
            cd /opt/boldreports/boldreports-package
            sudo bash install-boldreports.sh -i upgrade -u root -h "$IDP_URL" -n true
            echo "Bold Reports upgrade script executed successfully."
        else
            echo "Error: Unable to extract Idp URL from $CONFIG_FILE"
        fi
    else
        echo "Error: Configuration file $CONFIG_FILE not found."
    fi
fi

echo "Post-installation script completed."

# Set environment variables
export OPENSSL_CONF=/etc/ssl/
export DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=true