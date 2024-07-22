import argparse
from pathlib import Path
from dotenv import load_dotenv
from src.monitor_logger import setup_logging
from src.live_stream_tracker import LiveStreamDetector
from src.track_and_count import LiveStreamSafetyMonitor
from datetime import datetime

def main(logger, youtube_url: str, model_path: str):
    """
    Main execution function that detects hazards, sends notifications, and logs warnings.

    Args:
        logger (logging.Logger): A logger instance for logging messages.
        youtube_url (str): The URL of the YouTube live stream to monitor.
        model_path (str): The file path of the YOLOv8 model to use for detection.
    """
    # Initialise the live stream detector
    live_stream_detector = LiveStreamDetector(youtube_url, model_path)

    # Initialise the safety zone tracker
    zone_tracker = LiveStreamSafetyMonitor()

    # Use the generator function to process detections
    for ids, datas, frame, timestamp in live_stream_detector.generate_detections():
        # Process detections using the safety zone tracker
        tracking_result = zone_tracker.process_data(timestamp, ids, datas)
        
        # Log the results
        logger.info(f"Timestamp: {timestamp}")
        logger.info(f"IDs: {ids}")
        logger.info(f"Datas (xyxy format): {datas}")
        logger.info(f"Tracking result: {tracking_result}")
    
    # Release resources after processing
    live_stream_detector.release_resources()


if __name__ == '__main__':
    # Load environment variables from the specified .env file
    env_path = Path('.env')  # Adjust if your .env file is located elsewhere
    load_dotenv(dotenv_path=env_path)

    parser = argparse.ArgumentParser(description='Monitor a live stream for safety hazards using YOLOv8.')
    parser.add_argument('--url', type=str, required=True, help='YouTube video URL for monitoring')
    parser.add_argument('--model', type=str, default='models/pt/best_yolov8x.pt', help='Path to the YOLOv8 model')
    args = parser.parse_args()

    logger = setup_logging()  # Set up logging
    main(logger, args.url, args.model)