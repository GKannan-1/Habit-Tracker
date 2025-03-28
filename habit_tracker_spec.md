## Project: Habit Tracker Web App

A web-based habit tracking app that allows users to create, manage, and monitor their personal habits over time.

---

### User Stories

#### 1. As a user, I want to register and log in, so that I can access my personal habit tracking dashboard.

#### 2. As a user, I want to create new habits, so I can track the activities I care about.
- Each habit has:
  - A name (e.g., "Exercise")
  - An optional description
  - A frequency: `daily` or `weekly`

#### 3. As a user, I want to view a list of my habits, including how often I should do them and when I last completed each one.

#### 4. As a user, I want to mark a habit as completed, so I can track my progress over time.
- A habit can be marked completed for **today** or a specific date.
- You can only mark a habit **once per day** (or once per week, depending on frequency).

#### 5. As a user, I want to see my streak for each habit, so I can stay motivated.
- A streak is the number of consecutive days (or weeks) the habit has been completed according to its frequency.

#### 6. As a user, I want to delete or edit a habit, in case I change my goals or make a mistake.

---

### Data Model Overview (for reference)

#### Habit
- `name`
- `description`
- `frequency` (`daily` or `weekly`)
- `owner` (linked to a registered user)
- `created_at`

#### HabitLog
- `habit` (FK)
- `date_completed`

---

### Page/Feature List

1. **Home page** (with login/register links or dashboard redirect)
2. **Register / Login / Logout**
3. **Dashboard**:
   - List of habits
   - Quick buttons to mark as done
   - Show current streaks
4. **Habit detail page**
   - History of completions
   - Edit/delete habit
5. **Add new habit** form
6. **Mark habit as done** (can be done inline or via detail page)

---

### Optional Features (Bonus)
- Progress charts
- Email reminders (daily/weekly)
- Leaderboards (if multi-user focus)
- Public sharing of streaks
