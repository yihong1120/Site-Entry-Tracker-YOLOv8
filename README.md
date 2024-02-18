# Site-Entry-Tracker-YOLOv8

## Overview

The Site-Entry-Tracker-YOLOv8 is a sophisticated artificial intelligence model developed to enhance safety and operational efficiency on construction sites. Utilising the cutting-edge YOLOv8 algorithm, this tool has been meticulously trained to identify critical safety and logistical elements, including hardhats, safety vests, masks, vehicles, machinery, and safety cones.

The core functionality of this application revolves around the innovative use of safety cones to establish a virtual boundary at site entrances and exits. By recognising the central points between strategically placed cones, the system creates an imaginary line that serves as a threshold for tracking movements. This approach enables the automated counting of personnel, vehicles, and machinery, thereby facilitating real-time management and safety compliance.

## Installation

To set up the Site-Entry-Tracker-YOLOv8 on your local system, follow these steps:

1. Clone this repository to your local machine.
   ```
   git clone https://github.com/yihong1120/Site-Entry-Tracker-YOLOv8.git
   ```
2. Install the required dependencies.
   ```
   pip install -r requirements.txt
   ```
3. Follow the configuration instructions below to set up the environment.

## Configuration

Before deploying the tracker, ensure that two safety cones are positioned on either side of each site entrance or exit. The AI model will use these cones to generate the virtual tracking line.

1. Position the cameras to capture a clear view of the area between the cones.
2. Adjust the settings in the `config.yml` file to match the specifics of your site and camera setup.

## Usage

To start the tracking, execute the following command:

```
python track_entries.py
```

The system will automatically begin monitoring the defined areas, counting and logging each entry and exit of people, vehicles, and machinery.

## Contributing

Contributions to the Site-Entry-Tracker-YOLOv8 are welcome. Please follow the standard pull request process to propose improvements or submit bug fixes.

## License

This project is licensed under the AGPL-3.0 license - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgements

- Special thanks to the YOLOv8 development team for their outstanding object detection model.
- Gratitude to all contributors who have helped in refining the Site-Entry-Tracker-YOLOv8.
