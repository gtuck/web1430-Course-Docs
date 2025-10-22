# Ch. 12: Personal Portfolio One-Pager

## Description

Create a personal single-page site in CodePen that highlights who you are, what you do, and how to get in touch. You will combine clean HTML structure, purposeful styling, JavaScript polish to ship a sharable calling card page.

## Learning Objectives

- Organize a one-page layout with semantic HTML sections.
- Apply custom CSS or a lightweight framework to achieve a cohesive visual style.
- Present personal details, skills/projects, and contact links clearly.
- Publish and share a hosted CodePen pen.

## Setup (CodePen Only)

- Go to [CodePen.io](https://codepen.io/) and select `Create → New Pen`.
- Title the pen `Ch. 12 - Personal Portfolio` (or similar).
- Plan to use the HTML, CSS and JS panels.
- Optional: In `Settings → CSS`, add Bulma, Tailwind, Bootstrap, or other frameworks if you prefer not to write all styles by hand.

## Instructions

1) Build the HTML structure
- Use the template below as a starting point in the HTML panel. Replace the placeholder name, title, bio, project blurbs, links, and photo with your own information (required).

```html
<!-- Personal Webpage -->
<header>
  <h1>Your Name</h1>
  <p>Your title or tagline</p>
</header>

<section id="about">
  <img src="https://via.placeholder.com/150" alt="Profile photo">
  <h2>About Me</h2>
  <p>Introduce yourself with a brief bio that highlights your focus areas.</p>
</section>

<section id="projects">
  <h2>Skills & Projects</h2>
  <div class="grid">
    <div class="card">
      <h3>Highlight One</h3>
      <p>Describe a project, class assignment, or skill.</p>
    </div>
    <div class="card">
      <h3>Highlight Two</h3>
      <p>Use consistent formatting and explain the impact or tooling.</p>
    </div>
    <div class="card">
      <h3>Highlight Three</h3>
      <p>Add more cards if you have additional items to showcase.</p>
    </div>
  </div>
</section>

<footer>
  <p>Connect:
    <a href="https://github.com/yourhandle" target="_blank" rel="noopener">GitHub</a> |
    <a href="mailto:you@example.com">Email</a>
  </p>
</footer>
```

2) Style the page with CSS
- Add the following CSS in the CSS panel, then customize colors, spacing, fonts, hover states, etc., so the page feels personal.

```css
body {
  font-family: system-ui, sans-serif;
  margin: 0;
  background: #fafafa;
  color: #333;
}

header {
  text-align: center;
  background: #003366;
  color: white;
  padding: 3rem 1rem;
}

header h1 {
  margin: 0;
  font-size: 2.5rem;
}

#about {
  text-align: center;
  padding: 2rem 1rem;
}

#about img {
  border-radius: 50%;
  margin: 1rem 0;
  max-width: 200px;
}

#projects {
  background: white;
  padding: 2rem 1rem;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.card {
  background: #f0f4f8;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

footer {
  text-align: center;
  padding: 1.5rem;
  background: #003366;
  color: white;
}
```

3) Add interactivity
- If you want a simple hover animation, paste this in the JS panel or extend it with your own ideas. Avoid frameworks unless you add them via settings.

```js
document.querySelectorAll('.card').forEach((card) => {
  card.addEventListener('mouseover', () => (card.style.transform = 'scale(1.05)'));
  card.addEventListener('mouseout', () => (card.style.transform = 'scale(1)'));
});
```

4) Customize and polish
- Swap in a real headshot or avatar, refine colors/typography, ensure the layout works on mobile, and add extra sections (skills list, contact form, resume link) as needed.
- Update the footer links to point to at least two real destinations (GitHub, LinkedIn, portfolio, email, etc.).
- Verify that headings follow a logical hierarchy (`h1` once, followed by `h2` sections).

5) Save and share
- Click `Save` (top right) to make the pen public.
- In `Settings → Details`, fill in a concise description and relevant tags.
- Copy the `Share → Full Page View` URL for submission.

## Checkpoints

- Name, title/tagline, and photo (or avatar) display at the top of the page.
- About section communicates who you are in 2–4 sentences.
- Grid showcases at least three skills/projects with headings and descriptions.
- Footer (or contact section) links to active contact methods or profiles.
- CSS produces a cohesive, readable design without layout issues.
- JS gracefully enhances interactivity without breaking functionality.

## What to Submit

- The public CodePen URL for `Ch. 12 - Personal Portfolio`.
- A short note (in Canvas or the LMS submission) confirming that you customized the content with your own information and tested the page in Full Page View.
