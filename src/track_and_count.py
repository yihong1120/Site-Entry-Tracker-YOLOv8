import time
from typing import Tuple, List, Dict, Union

class LiveStreamSafetyMonitor:
    """A class to track the entry and exit of people, vehicles, and machinery based on safety cone demarcations."""

    PERSON: float = 5.0
    VEHICLE: float = 9.0
    MACHINERY: float = 8.0
    SAFETY_CONE: float = 6.0

    def __init__(self):
        """Initialises the tracker with default values."""
        self.entry_count = {'Person': 0, 'Vehicle': 0, 'Machinery': 0}
        self.exit_count = {'Person': 0, 'Vehicle': 0, 'Machinery': 0}
        self.last_cone_positions = []  # Last known positions of the safety cones
        self.last_line_time = time.time()  # Time when the last line was defined

    def update_cone_positions(self, ids: List[float], datas: List[List[float]]):
        """
        Updates the positions of safety cones used to define the boundary line.

        Args:
            ids (List[float]): The list of detected object IDs.
            datas (List[List[float]]): The detection data.
        """
        current_time = time.time()
        cone_positions = [data[:4] for data, id in zip(datas, ids) if id == self.SAFETY_CONE]
        
        if len(cone_positions) == 2:
            self.last_cone_positions = cone_positions
            self.last_line_time = current_time

    def get_line_equation(self) -> Union[Tuple[float, float], None]:
        """
        Computes the line equation from the safety cones' positions.

        Returns:
            Union[Tuple[float, float], None]: The gradient and intercept of the line, or None if not defined.
        """
        if len(self.last_cone_positions) == 2:
            x1, y1 = (self.last_cone_positions[0][0] + self.last_cone_positions[0][2]) / 2, self.last_cone_positions[0][3]
            x2, y2 = (self.last_cone_positions[1][0] + self.last_cone_positions[1][2]) / 2, self.last_cone_positions[1][3]
            m = (y2 - y1) / (x2 - x1)
            c = y1 - m * x1
            return m, c
        return None

    def update_counts(self, m: float, c: float, datas: List[List[float]]):
        """
        Updates the entry and exit counts based on the detected objects' positions relative to the boundary line.

        Args:
            m (float): The gradient of the line.
            c (float): The intercept of the line.
            datas (List[List[float]]): The detection data.
        """
        for data in datas:
            x_center = (data[0] + data[2]) / 2
            y_bottom = data[3]
            object_id = data[4]
            y_line_at_x = m * x_center + c

            if object_id in [self.PERSON, self.VEHICLE, self.MACHINERY]:
                category = 'Person' if object_id == self.PERSON else 'Vehicle' if object_id == self.VEHICLE else 'Machinery'
                if y_bottom > y_line_at_x:  # Object crossing from above to below the line
                    self.entry_count[category] += 1
                elif y_bottom < y_line_at_x:  # Object crossing from below to above the line
                    self.exit_count[category] += 1

    def process_data(self, timestamp: float, ids: List[float], datas: List[List[float]]) -> Union[Dict[str, int], str]:
        """
        Processes a batch of detection data to update entry and exit counts.

        Args:
            timestamp (float): The timestamp of the detection.
            ids (List[float]): The list of detected object IDs.
            datas (List[List[float]]): The detection data.

        Returns:
            Union[Dict[str, int], str]: The updated counts of entries and exits, or a pause message.
        """
        self.update_cone_positions(ids, datas)
        line_eq = self.get_line_equation()

        if time.time() - self.last_line_time > 3600:  # Check if it has been more than an hour without new cones
            return "Paused: No valid line defined for the last hour."

        if line_eq is None:
            return "Paused: No line defined."

        m, c = line_eq
        self.update_counts(m, c, datas)

        return self.entry_count, self.exit_count

if __name__ == '__main__':
    # Example usage
    tracker = LiveStreamSafetyMonitor()
    timestamp = 1708774114.949325
    ids = [7.0]
    datas = [[230.9345245361328, 225.36647033691406, 291.2240905761719, 257.8404541015625, 7.0, 0.4151361882686615, 2.0]]
    result = tracker.process_data(timestamp, ids, datas)
    print(result)
