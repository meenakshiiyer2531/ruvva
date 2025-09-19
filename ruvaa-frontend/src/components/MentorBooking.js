import React, { useState } from "react";

function MentorBooking() {
  const mentorsList = [
    { name: "Dr. Meenakshi", philosophy: "Learning through curiosity and practice" },
    { name: "Mr. Sharma", philosophy: "Focus on problem-solving and creativity" },
    { name: "Ms. Kapoor", philosophy: "Guidance with patience and empathy" },
  ];

  const [form, setForm] = useState({
    studentName: "",
    date: "",
    mentorName: "",
  });

  const [bookings, setBookings] = useState([]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleBook = () => {
    if (!form.studentName || !form.date || !form.mentorName) {
      return alert("❌ Please fill all fields");
    }

    const mentor = mentorsList.find(m => m.name === form.mentorName);

    const newBooking = {
      studentName: form.studentName,
      date: form.date,
      mentorName: form.mentorName,
      philosophy: mentor ? mentor.philosophy : "",
    };

    setBookings([...bookings, newBooking]);
    alert(`✅ Mentor session booked with ${form.mentorName} on ${form.date}`);
    setForm({ studentName: "", date: "", mentorName: "" });
  };

  return (
    <div className="min-h-screen w-full bg-gradient-to-r from-blue-200 via-purple-200 to-pink-200 flex flex-col items-center justify-start py-10 px-4 md:px-16 lg:px-32">
      <h1 className="text-5xl font-bold text-gray-800 mb-10 animate-pulse text-center">📅 Book Your Mentor</h1>

      <div className="w-full max-w-4xl bg-white/80 backdrop-blur-md rounded-3xl shadow-2xl p-10 flex flex-col space-y-8">
        <input
          name="studentName"
          placeholder="Your Name"
          value={form.studentName}
          onChange={handleChange}
          className="w-full px-6 py-4 rounded-xl border-2 border-gray-300 focus:border-blue-500 focus:outline-none transition text-lg"
        />

        <input
          type="date"
          name="date"
          value={form.date}
          onChange={handleChange}
          className="w-full px-6 py-4 rounded-xl border-2 border-gray-300 focus:border-blue-500 focus:outline-none transition text-lg"
        />

        <select
          name="mentorName"
          value={form.mentorName}
          onChange={handleChange}
          className="w-full px-6 py-4 rounded-xl border-2 border-gray-300 focus:border-blue-500 focus:outline-none transition text-lg"
        >
          <option value="">Select Mentor</option>
          {mentorsList.map((mentor, idx) => (
            <option key={idx} value={mentor.name}>
              {mentor.name} — {mentor.philosophy}
            </option>
          ))}
        </select>

        <button
          onClick={handleBook}
          className="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-4 rounded-xl transition transform hover:scale-105 text-xl"
        >
          Book Session
        </button>
      </div>

      {bookings.length > 0 && (
        <div className="w-full max-w-5xl mt-12 space-y-6 px-4 md:px-8 lg:px-16">
          <h2 className="text-3xl font-semibold text-gray-800 mb-6 text-center">📋 Your Bookings</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {bookings.map((b, idx) => (
              <div key={idx} className="bg-white/80 backdrop-blur-md p-6 rounded-2xl shadow-xl transition hover:scale-105">
                <p className="text-lg"><strong>Student:</strong> {b.studentName}</p>
                <p className="text-lg"><strong>Date:</strong> {b.date}</p>
                <p className="text-lg"><strong>Mentor:</strong> {b.mentorName}</p>
                <p className="text-md text-gray-600"><strong>Philosophy:</strong> {b.philosophy}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default MentorBooking;
