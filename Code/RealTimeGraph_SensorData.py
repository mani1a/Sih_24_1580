import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import firebase_admin
from firebase_admin import credentials, firestore
import threading
import datetime

# Initialize Firebase
key = credentials.Certificate('sih-24-firebase-adminsdk-j4i85-5054a37af1.json')
firebase_admin.initialize_app(key)

# Threading lock to manage data access
data_lock = threading.Lock()

# Firebase Firestore client
db = firestore.client()

# Lists to store data
timestamps = []
accX = []
accY = []

def fetching_data(snapshot, changes, read_time):
    global timestamps, accX, accY
    with data_lock:
        for doc in snapshot:
            data = doc.to_dict()
            acc_x = data.get('acc_x')
            acc_y = data.get('acc_y')
            timestamp = data.get('timestamp')  

            if timestamp:
                timestamps.append(datetime.datetime.fromtimestamp(timestamp))
            else:
                timestamps.append(datetime.datetime.now())  #current time
            
            accX.append(acc_x)
            accY.append(acc_y)

# Firebase query and snapshot listener
query = db.collection('Mani').document('SensorData')
query_watch = query.on_snapshot(fetching_data)

# Create a figure and axis
fig, ax = plt.subplots()
line1, = ax.plot([], [], label="accX")
line2, = ax.plot([], [], label="accY")

ax.set_xlabel("Time")
ax.set_ylabel("Acceleration")
ax.legend()

# Function to update the data for animation
def update(frame):
    with data_lock:
        # Update the data for the plot
        if timestamps:
            line1.set_data(timestamps, accX)
            line2.set_data(timestamps, accY)
            
            ax.relim()   # Recalculate limits
            ax.autoscale_view()  # Rescale view to fit new data

    return line1, line2

# Create an animation object
ani = animation.FuncAnimation(fig, update, interval=100)

# Show the plot
plt.show()
