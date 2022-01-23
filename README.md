[![HACS Custom][hacs_shield]][hacs]
[![GitHub Latest Release][releases_shield]][latest_release]
[![GitHub All Releases][downloads_total_shield]][releases]
[![Buy me a coffee][buy_me_a_coffee_shield]][buy_me_a_coffee]
[![PayPal.Me][paypal_me_shield]][paypal_me]


[hacs_shield]: https://img.shields.io/static/v1.svg?label=HACS&message=Custom&style=popout&color=orange&labelColor=41bdf5&logo=HomeAssistantCommunityStore&logoColor=white
[hacs]: https://hacs.xyz/docs/default_repositories

[latest_release]: https://github.com/PiotrMachowski/Home-Assistant-custom-components-Dom-5/releases/latest
[releases_shield]: https://img.shields.io/github/release/PiotrMachowski/Home-Assistant-custom-components-Dom-5.svg?style=popout

[releases]: https://github.com/PiotrMachowski/Home-Assistant-custom-components-Dom-5/releases
[downloads_total_shield]: https://img.shields.io/github/downloads/PiotrMachowski/Home-Assistant-custom-components-Dom-5/total

[buy_me_a_coffee_shield]: https://img.shields.io/static/v1.svg?label=%20&message=Buy%20me%20a%20coffee&color=6f4e37&logo=buy%20me%20a%20coffee&logoColor=white
[buy_me_a_coffee]: https://www.buymeacoffee.com/PiotrMachowski

[paypal_me_shield]: https://img.shields.io/static/v1.svg?label=%20&message=PayPal.Me&logo=paypal
[paypal_me]: https://paypal.me/PiMachowski

# Dom 5 Sensor

This custom integration retrieves data from [Dom 5](https://www.sacer.pl/dom5) - housing cooperative management system.

## Installation

### Using [HACS](https://hacs.xyz/) (recommended)

This integration can be added to HACS as a [custom repository](https://hacs.xyz/docs/faq/custom_repositories):
* URL: `https://github.com/PiotrMachowski/Home-Assistant-custom-components-Dom-5`
* Category: `Integration`

After adding a custom repository you can use HACS to install this integration using user interface.

### Manual

To install this integration manually you have to download [*dom_5.zip*](https://github.com/PiotrMachowski/Home-Assistant-custom-components-Dom-5/releases/latest/download/dom_5.zip) and extract its contents to `config/custom_components/dom_5` directory:
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

## Displaying data
You can display data from this integration using [Markdown card](https://www.home-assistant.io/lovelace/markdown/):

```yaml
type: markdown
content: |-
  {%- set username="123456" -%}
  # Latest announcement
  ## {{ state_attr('sensor.dom_5_last_announcement_' + username, 'title') }}
  {{ state_attr('sensor.dom_5_last_announcement_' + username, 'body') }}
  ---  
  # Latest message
  ## {{ state_attr('sensor.dom_5_last_message_' + username, 'title') }}  
  {{ state_attr('sensor.dom_5_last_message_' + username, 'body') }}
  ---
  # Finances
  **Balance:** {{ "%.2f zł" | format(states('sensor.dom_5_finances_' + username) | float) }}
  **Arrear:** {{ "%.2f zł" | format(state_attr('sensor.dom_5_finances_' + username, 'arrear') | float) }}
  **Overpayment:** {{ "%.2f zł" | format(state_attr('sensor.dom_5_finances_' + username, 'overpayment') | float) }}
  ```

<a href="https://www.buymeacoffee.com/PiotrMachowski" target="_blank"><img src="https://bmc-cdn.nyc3.digitaloceanspaces.com/BMC-button-images/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>
<a href="https://paypal.me/PiMachowski" target="_blank"><img src="https://www.paypalobjects.com/webstatic/mktg/logo/pp_cc_mark_37x23.jpg" border="0" alt="PayPal Logo" style="height: auto !important;width: auto !important;"></a>
