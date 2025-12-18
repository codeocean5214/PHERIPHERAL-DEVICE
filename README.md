# Environment Monitoring and Security System

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/codeocean5214/PHERIPHERAL-DEVICE.git
   ```
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Download the pre-trained face recognition model:
   ```
   python model_load.py
   ```

## Usage

1. Register a new face:
   ```
   python registeration.py
   ```
   This will capture 10 samples of your face and save the embeddings to `embeddings.npy`.
2. Run the main application:
   ```
   python main.py
   ```
   This will start the environment monitoring and security system.

## API

The system consists of the following modules:

1. `Environment`:
   - `get_data()`: Returns a dictionary with the current environmental data (room temperature, humidity, pressure, and body temperature).

2. `SecurityChecks`:
   - `detected_motion`: Returns `True` if motion is detected.
   - `lock_door()`: Locks the door.
   - `unlock_door()`: Unlocks the door.

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Implement your changes.
4. Test your changes.
5. Submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Testing

To run the tests, execute the following command:
```
python -m unittest discover tests
```
