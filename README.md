[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz/docs/faq/custom_repositories)
[![buymeacoffee_badge](https://img.shields.io/badge/Donate-Buy%20Me%20a%20Coffee-ff813f?style=flat)](https://www.buymeacoffee.com/PiotrMachowski)
[![paypalme_badge](https://img.shields.io/badge/Donate-PayPal-0070ba?style=flat)](https://paypal.me/PiMachowski)
![GitHub All Releases](https://img.shields.io/github/downloads/PiotrMachowski/Home-Assistant-custom-components-Dom-5/total)

# Dom 5 Sensor

This custom integration retrieves data from [Dom 5](https://www.sacer.pl/dom5) - housing cooperative management system.

## Installation

### Using [HACS](https://hacs.xyz/) (recommended)

This integration can be added to HACS as a [custom repository](https://hacs.xyz/docs/faq/custom_repositories):
* URL: `https://github.com/PiotrMachowski/Home-Assistant-custom-components-Dom-5`
* Category: `Integration`

After adding a custom repository you can use HACS to install this integration using user interface.

### Manual

To install this integration manually you have to download [*dom_5.zip*](https://github.com/PiotrMachowski/Home-Assistant-custom-components-Dom-5/releases/latest/download/dom_5.zip) extract its contents to `config/custom_components/dom_5` directory:
```bash
mkdir -p custom_components/dom_5
cd custom_components/dom_5
wget https://github.com/PiotrMachowski/Home-Assistant-custom-components-Dom-5/releases/latest/download/dom_5.zip
unzip dom_5.zip
rm dom_5.zip
```

## Configuration

### Config flow (recommended)

To configure this integration go to: _Configuration_ -> _Integrations_ -> _Add integration_ -> _Dom 5_.

You can also use following [My Home Assistant](http://my.home-assistant.io/) link

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=dom_5)

### Manual - yaml
| Key | Type | Required | Value | Description |
|---|---|---|---|---|
| `platform` | string | true | `dom_5` | Name of a platform |
| `name` | string | false |   | Desired name of a entity |
| `url` | string | true |   | URL of system (in format: `https://dom5.pl` |
| `username` | string | true |   | Username in Dom 5 system |
| `password` | string | true |   | Password in Dom 5 system |

#### Example configuration
```yaml
sensor:
  - platform: dom_5
    url: "https://dom5.pl"
    username: "123456"
    password: "SecretPassword"
```


<a href="https://www.buymeacoffee.com/PiotrMachowski" target="_blank"><img src="https://bmc-cdn.nyc3.digitaloceanspaces.com/BMC-button-images/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>
