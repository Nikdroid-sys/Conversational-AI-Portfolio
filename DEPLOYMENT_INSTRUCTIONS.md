# Akasha: Deployment Instructions

I have completed the transformation of your project into "Akasha." The futuristic holographic UI is implemented, the Vedic sage persona is embedded in the backend, and the project has been fully committed to your local git repository.

Your application is now ready to be shared with the world. Here are the final steps to get your portfolio live on GitHub Pages:

### Step 1: Create a Repository on GitHub

1.  Go to [GitHub](https://github.com) and log in.
2.  Click the **+** icon in the top right corner and select **"New repository"**.
3.  Name your repository (e.g., `akasha-chatbot`). **This name is important!**
4.  Choose "Public" for visibility.
5.  Click **"Create repository"**.

### Step 2: Push Your Local Project to GitHub

On the new repository page, GitHub will show you a URL. Copy it. It will look like `https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPOSITORY_NAME>.git`.

Now, in your local terminal in the `d:\ai-chatbot` directory, run the following commands, replacing the placeholder with your copied URL:

```bash
# Link your local repo to the remote one on GitHub
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPOSITORY_NAME>.git

# Rename your branch to 'main' if it's not already
git branch -M main

# Push your code to GitHub
git push -u origin main
```

### Step 3: Configure for Deployment

I have already prepared your project for deployment. However, you need to make two small but **critical** edits:

1.  **In `frontend/package.json`:**
    *   Change the `"homepage"` value from `https://<YOUR_GITHUB_USERNAME>.github.io/<YOUR_REPOSITORY_NAME>` to your actual GitHub username and repository name.

2.  **In `frontend/vite.config.ts`:**
    *   Change the `base` value from `"/<YOUR_REPOSITORY_NAME>/"` to your repository name (e.g., `"/akasha-chatbot/"`).

After editing, save the files and commit the changes:

```bash
git add frontend/package.json frontend/vite.config.ts
git commit -m "chore: Finalize GitHub Pages deployment configuration"
git push
```

### Step 4: Deploy Akasha

You are now ready to deploy. In your terminal, navigate to the `frontend` directory and run:

```bash
# This will build and deploy your application
npm run deploy
```

This command will create a `gh-pages` branch on your GitHub repository and push the built application files to it.

### Step 5: See Your Project Live!

After a minute or two, your live application will be available at the URL you configured in `package.json`. You can also find the URL in your repository's settings under **Pages**.

Your portfolio piece, **Akasha**, is now complete and online. Congratulations!
