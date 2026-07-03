# Career Field Notes — Quick Start

## Project Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Opens at `http://localhost:8501`

## What You Have Now

- ✓ **models.py**: Student, EntryResponse, 6 entry templates
- ✓ **persistence.py**: File-based JSON storage (students.json, responses.json)
- ✓ **app.py**: Full Streamlit app with 4 screens:
  - Join (sign in)
  - Home/Trail (entry list, unlock logic)
  - Entry detail (fill prompts, save/complete)
  - Notebook (view all entries + Entry 1 vs Entry 6)

## Test Flow (5 min)

1. Sign in (any name + class code)
2. See Trail with 6 locked entries (Entry 1 open)
3. Click Entry 1, fill the prompts, click "Mark Complete"
4. See Entry 2 unlock on home screen
5. Go to Notebook, see Entry 1 in the journal
6. Sign out, sign back in with same credentials to verify data persists

## Data Stored

```
data/
  students.json      # name, class_code, created_date
  responses.json     # entry fields, status, timestamp
```

## Next Steps (in order)

1. **Test locally** — run the app, walk through join → entry → notebook
2. **PDF export** — add reportlab to show_notebook() to generate PDF
3. **Mobile test** — open `localhost:8501` on phone, test buttons + form
4. **Deploy** — push to Streamlit Cloud or Vercel
5. **Iterate** — feedback from first users, refine language, add celebrations

## Troubleshooting

- **Module not found**: `pip install -r requirements.txt`
- **Port 8501 in use**: `streamlit run app.py --server.port 8502`
- **Data not saving**: Check `data/` folder exists (app creates it)

## Code Map

- Entry 1 has product feedback prompts (field 6)
- Entry 6 has closing feedback prompt (field 7)
- These feed product signal (extract in next phase)
- Unlock logic: entry N needs entry N-1 = "done"

Good to go. Test it. 🚀
