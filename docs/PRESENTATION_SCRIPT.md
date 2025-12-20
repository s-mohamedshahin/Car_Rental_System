# Phase 5: Final Presentation & Demo Script

**Time Limit**: ~5-10 Minutes
**Goal**: Show that the system works, meets requirements, and is built correctly.

---

## Part 1: Introduction (Slide 1-2)
* **Say**: "Good morning/afternoon. We are Team [Name]. Today we are presenting the final delivery of our Car Rental System."
* **Say**: "Our application allows users to browse, search, and rent cars. It is built using **Flask** and follows the **MVC architecture** strictly."
* **Highlight**: "We have fully containerized the app using **Docker**, and we have a 100% automated test suite running on GitHub Actions."

---

## Part 2: The Live Demo (Screen Share)

### Step 1: Helper / Docker (Show Terminal)
* **Action**: Show your terminal with `docker-compose up` running.
* **Say**: "As you can see, the application is running entirely inside a Docker container. The database is also persistent."

### Step 2: Browsing & Filtering (Show Browser)
* **Action**: Open `http://localhost:5000`.
* **Say**: "Here is the main landing page. It redirects to the car listing."
* **Action**: Click filter "Brand: Toyota" and "Search".
* **Say**: "We can filter by Brand. You see only Toyotas now."
* **Action**: Click "Availability: Available" and "Search".
* **Say**: "We can also filter to show only cars that are currently available."

### Step 3: Car Details (Show Browser)
* **Action**: Click on "View Details" for one car.
* **Say**: "This is the details page. It shows all specifications including GPS, Type, and Rental Rate."

### Step 4: API & Architecture (Show Postman or Code)
* **Action**: Briefly switch to VS Code to show `models.py` or just mention it.
* **Say**: "Behind the scenes, the Controller logic is separated from the Views. For example, updating a status constitutes a business logic transaction handled by the `CarController` class."
* **Optional**: Run a `curl` or Postman request to update status if asked.

---

## Part 3: Technical Quality (Slides)

### Testing
* **Say**: "We didn't just write code; we ensured it works. We have **15+ automated tests**."
* **Show**: A screenshot of the GitHub Actions green checkmark or the test coverage report (98%).

### CI/CD
* **Say**: "Our CI/CD pipeline runs on every push. It builds the Docker image and runs all tests automatically."

---

## Part 4: Conclusion
* **Say**: "In conclusion, we have delivered a fully functional, tested, and containerized Car Rental System that meets all the SRS functional and non-functional requirements."
* **Ask**: "Thank you. Any questions?"
