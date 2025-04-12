
const express = require('express');
const cors = require('cors');
const multer = require('multer');
const mongoose = require('mongoose');
const parseResume = require('./utils/parserClient');
require('dotenv').config();

const app = express();
const upload = multer();

app.use(cors());
app.use(express.json());

// MongoDB Connection
mongoose.connect(process.env.MONGODB_URI || "mongodb://localhost:27017/ats", {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

// Candidate Schema
const CandidateSchema = new mongoose.Schema({
  name: String,
  email: String,
  phone: String,
  dob: String,
  location: {
    city: String,
    state: String,
    country: String
  },
  skills: [String],
  certifications: [String],
  summary: String,
  score: Number,
  resume: Buffer,
  note: String,
  status: String
});

const Candidate = mongoose.model('Candidate', CandidateSchema);

// Upload and Parse Resume
app.post('/api/candidates', upload.single('resume'), async (req, res) => {
  try {
    const file = req.file;
    const parsed = await parseResume(file.buffer, file.originalname);

    const duplicate = await Candidate.findOne({ email: parsed.email });
    if (duplicate) return res.status(409).json({ message: "Duplicate candidate found" });

    const candidate = new Candidate({
      name: parsed.name,
      email: parsed.email,
      phone: parsed.phone,
      dob: parsed.dob,
      location: parsed.location,
      skills: parsed.skills,
      certifications: parsed.certifications,
      summary: parsed.summary,
      score: parsed.score,
      resume: file.buffer,
      note: '',
      status: 'Screening'
    });

    await candidate.save();
    res.status(201).json({ message: "Candidate saved", data: candidate });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: "Error parsing resume", error: err.message });
  }
});

// Start server
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
