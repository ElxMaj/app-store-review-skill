# FocusNest product evidence

## Product and audience

FocusNest is described as "a beautiful focus timer for everyone." The intended launch audience is freelancers, but no workflow currently uses client work, deadlines, estimates, invoices, projects, or another freelancer-specific object.

The first session is:

1. Swipe through three onboarding pages: "Focus better", "Build habits", and "Reach your goals".
2. Accept the notification permission request.
3. Choose 25, 45, or 60 minutes.
4. Tap Start on a circular timer.
5. Mark the session complete and add one sentence of notes.

History shows completed sessions by day. A streak increases when at least one session is completed. "Focus Score" is the percentage of started sessions that reached zero. All data is stored locally in UserDefaults. There are no project, planning, calendar, collaboration, automation, or domain-specific features.

## Provenance supplied by the developer

Mara purchased the commercial "Swift Focus Timer UI Kit" and kept its four-tab navigation, circular timer component, settings layout, SF Symbol choices, and bundled completion sounds. She changed the name, type scale, and palette. The app icon recolors the kit's layered hourglass SVG but keeps its paths and silhouette. The template license permits one commercial app.

The timer logic and history calculations were written for FocusNest. The app uses SwiftUI and no cross-platform framework. Mara has no other focus apps in her developer account. No archive, repository history, exact asset comparison, or copy of another submitted binary was supplied.

## Screen review notes

- **Today:** coral-to-purple background, large circular timer, Start button, streak count, and a rotating motivational quote.
- **History:** calendar heat map using green for completed days and red for missed days. There is no non-color status label.
- **Statistics:** three charts. Before three sessions, the screen says "No data".
- **Settings:** rows for Notifications, Sounds, Theme, Rate the App, Privacy, and Restore Defaults.
- **Completion:** confetti, a medium haptic, and "Great job! You crushed it."
- **Errors and recovery:** there are no documented error, interrupted-timer, notification-denied, or data-reset recovery states.
- **iPad:** the phone layout is centered at full height with large empty margins. Split View and keyboard use were not tested.
- **Accessibility:** VoiceOver labels exist for Start and Pause. Dynamic Type, Reduce Motion, increased contrast, and color-blind status recognition were not tested on a device.

## Draft App Store page

- **Name:** FocusNest: Focus Timer
- **Subtitle:** Focus timer & habit tracker
- **First sentence:** "Unlock the power of focus and achieve more every day with the ultimate productivity companion."
- **Screenshot captions:** "Focus. Grow. Repeat.", "Build better habits", "See your progress", "Stay motivated", and "Become your best self".
- **Keywords:** focus,timer,pomodoro,productivity,habits,study,work
- **What's New:** Initial release.

The screenshot mockups show the Today timer, History calendar, and Statistics charts described above. No competitor comparison, real iPad screenshot, support-page content, or App Store search review was supplied.

## Developer concern

Mara used coding assistants for parts of the Swift implementation. She asks whether Apple can detect that the app was "made with AI" and whether changing the color palette or adding animations would be enough to avoid a 4.3(b) rejection.
