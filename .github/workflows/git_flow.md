# Git flow

1. ``main`` branch **1.0.0-SAPSHOT**
2. Create a branch called `release/1.0.X` **1.0.1-SNAPSHOT**
3. Release the branch `release/1.0.X`:
   1. Create a tag: `V1.0.0` **1.0.0**
   2. Increment version of the release branch `release/1.0.X` **1.0.2-SNAPSHOT**
   3. Deploy the tag `V1.0.0` (**1.0.0**) on `UAT`
   4. Do some dev
   5. Merge it on main and on all versions >1.0.x
   6. Create a tag `V1.0.1` **1.0.1**
   7. Increment version of the release branch `release/1.0.X` **1.0.2-SNAPSHOT** 
   8. Deploy the tag `V1.0.1` (**1.0.1**) on `UAT`
4. GO-LIVE 
   1. Deploy the tag `V1.0.1` (**1.0.1**) on `PROD`