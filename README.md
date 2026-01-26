

---

# 🌌 Aurora Camp Server (Knack MCP)

Aurora Camp Server is a **Model Context Protocol (MCP)** server built using **FastMCP**, designed to manage the Aurora winter camp operations Knack APP through the **Knack API**.
It enables AI agents or tools to search, create, update, and manage camps, bookings, and enrolled children in a structured and secure way.

---

## ✨ Features

* 🔍 Search camps by category, capacity, or location
* 🏕️ Create, update, and delete camp records
* 📅 Handle date & time ranges in Knack-compatible format
* 👶 List enrolled children per camp
* ➕ Add children to parent profiles
* 📦 Retrieve bookings and availability
* 🔐 Secure API access via environment variables
* 🤖 Fully MCP-compatible for AI tool integration

---

## 🏗️ Architecture Overview

* **Framework:** `FastMCP`
* **Backend API:** Knack REST API
* **Language:** Python 3.9+


---



## 🧠 MCP Tools Available

### 🔍 `search_camps`

Search winter camps with optional filters.

**Parameters**

* `category` (Art, Sports, STEM, Nature)
* `min_capacity`
* `location`

---

### 🏕️ `get_camp`

Fetch detailed camp information by name.

**Parameters**

* `camp_name`

---

### ➕ `create_camp`

Create a new winter camp.

**Required Parameters**

* `name`
* `category`
* `start_date`, `end_date` (YYYY-MM-DD)
* `start_time`, `end_time` (HH:MM AM/PM)
* `capacity`
* `location_street`, `location_city`, `location_state`, `location_zip`
* `provider_id`
* `description`

---

### ✏️ `update_camp`

Update an existing camp.

**Parameters**

* `camp_id`
* `name` (optional)
* `category` (optional)
* `capacity` (optional)
* `description` (optional)

---

### 🗑️ `delete_camp`

Delete a camp by camp ID.

**Parameters**

* `camp_id`

---

### 👶 `list_child`

List enrolled children for a given camp.

**Parameters**

* `camp_name`

---

### ➕👧 `add_child`

Add a child under a parent profile.

**Parameters**

* `parent`
* `child_name`
* `child_age`
* `child_date_of_birth` (optional)
* `diet_res` (optional)
* `emergency_contact` (optional)

---

### 📦 `get_bookings`

Retrieve all bookings for a camp.

**Parameters**

* `camp_id`

---

### 📊 `get_camp_availability`

Check available spots for a camp.

**Parameters**

* `camp_id`

---

## 🧩 Date Handling

The server automatically converts human-readable dates and times into Knack’s required format using:

```python
format_date_range()
```

This ensures consistency across all camp schedules.

---

## 🛠️ Future Enhancements

* Parent & provider creation tools
* Booking creation & cancellation
* Payment status syncing
* Camp analytics & reporting
* Role-based access control

---

## 📜 License

MIT License — free to use, modify, and distribute.

---

 This was done for the Contra Holiday Challenge 2025