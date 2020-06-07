# Header file for system mode object
class SystemStatus():
    def __init__(self):
        print("Sourdough Starter Feeder")
        print("Project by Timothy Moore")
        print()
        print("Initialising system mode as manual...")
        try:
            self.Mode = "manual"
            if (self.Mode == "manual"):
                print("Setup complete. Waiting on input...")
                print()
        except:
            print("Setup failed")
            pass
    
    def update(self, mode):
        self.Mode = mode
        print(self.Mode)
        print()
