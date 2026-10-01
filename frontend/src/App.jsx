import { useRef, useState } from "react";
import "./App.css";

const API_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

function App() {
  // =====================================================
  // STATE
  // =====================================================

  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: "bot",
      text: "Hello! I'm your AI Car Mechanic. Tell me what's wrong with your car.",
    },
  ]);

  const [input, setInput] = useState("");
  const [conversationId, setConversationId] = useState(null);

  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);

  // =====================================================
  // DIAGNOSIS STATE
  // =====================================================

  const [canDiagnose, setCanDiagnose] = useState(false);
  const [diagnosisGenerated, setDiagnosisGenerated] = useState(false);

  // =====================================================
  // BOOKING STATE
  // =====================================================

  const [showBookingForm, setShowBookingForm] = useState(false);
  const [bookingLoading, setBookingLoading] = useState(false);
  const [bookingResult, setBookingResult] = useState(null);

  const [bookingForm, setBookingForm] = useState({
    customer_name: "",
    phone: "",
    vehicle: "",
    service: "",
    preferred_date: "",
    preferred_time: "",
  });

  const fileInputRef = useRef(null);

  // =====================================================
  // SEND CHAT MESSAGE
  // =====================================================

  const sendMessage = async () => {
    const text = input.trim();

    if (!text || loading || uploading || diagnosisGenerated) {
      return;
    }

    // Add user message to UI immediately
    const userMessage = {
      id: Date.now(),
      sender: "user",
      text: text,
    };

    setMessages((previousMessages) => [
      ...previousMessages,
      userMessage,
    ]);

    setInput("");
    setLoading(true);

    try {
      const requestBody = {
        message: text,
      };

      // Send conversation ID for subsequent messages
      if (conversationId !== null) {
        requestBody.conversation_id = conversationId;
      }

      const response = await fetch(`${API_URL}/api/chat/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.error || "Unable to process your message."
        );
      }

      // Save conversation ID returned by Django
      setConversationId(data.conversation_id);

      // =================================================
      // DIAGNOSIS AVAILABILITY
      // =================================================

      setCanDiagnose(data.needs_follow_up === false);

      // =================================================
      // ADD DJANGO RESPONSE
      // =================================================

      const botMessage = {
        id: Date.now() + 1,
        sender: "bot",
        text: data.response,
      };

      setMessages((previousMessages) => [
        ...previousMessages,
        botMessage,
      ]);
    } catch (error) {
      console.error("Chat API error:", error);

      setMessages((previousMessages) => [
        ...previousMessages,
        {
          id: Date.now() + 1,
          sender: "bot",
          text: `Sorry, I couldn't connect to the mechanic service. ${error.message}`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  // =====================================================
  // ENTER KEY
  // =====================================================

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  // =====================================================
  // OPEN FILE SELECTOR
  // =====================================================

  const openFileSelector = () => {
    if (!conversationId) {
      alert(
        "Please send a message first so a conversation can be created."
      );

      return;
    }

    if (diagnosisGenerated) {
      return;
    }

    fileInputRef.current?.click();
  };

  // =====================================================
  // MEDIA TYPE DETECTION
  // =====================================================

  const getMediaType = (file) => {
    if (file.type.startsWith("image/")) {
      return "image";
    }

    if (file.type.startsWith("audio/")) {
      return "audio";
    }

    if (file.type.startsWith("video/")) {
      return "video";
    }

    return null;
  };

  // =====================================================
  // MEDIA UPLOAD
  // Supports:
  // IMAGE
  // AUDIO
  // VIDEO
  // =====================================================

  const handleFileChange = async (event) => {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    if (!conversationId) {
      alert("Please send a message first.");
      event.target.value = "";
      return;
    }

    if (diagnosisGenerated) {
      event.target.value = "";
      return;
    }

    // =================================================
    // DETERMINE MEDIA TYPE
    // =================================================

    const mediaType = getMediaType(file);

    if (!mediaType) {
      alert(
        "Please select an image, audio, or video file."
      );

      event.target.value = "";
      return;
    }

    // =================================================
    // MAX FILE SIZE
    //
    // 10 MB for images
    // 25 MB for audio
    // 50 MB for video
    // =================================================

    let maxSize;
    let maxSizeText;

    if (mediaType === "image") {
      maxSize = 10 * 1024 * 1024;
      maxSizeText = "10 MB";
    } else if (mediaType === "audio") {
      maxSize = 25 * 1024 * 1024;
      maxSizeText = "25 MB";
    } else {
      maxSize = 50 * 1024 * 1024;
      maxSizeText = "50 MB";
    }

    if (file.size > maxSize) {
      alert(
        `${
          mediaType.charAt(0).toUpperCase() +
          mediaType.slice(1)
        } must be smaller than ${maxSizeText}.`
      );

      event.target.value = "";
      return;
    }

    setUploading(true);

    try {
      const formData = new FormData();

      // =================================================
      // FORM DATA
      // =================================================

      formData.append(
        "conversation_id",
        conversationId
      );

      formData.append(
        "media_type",
        mediaType
      );

      formData.append(
        "file",
        file
      );

      // =================================================
      // UPLOAD TO DJANGO
      // =================================================

      const response = await fetch(
        `${API_URL}/api/upload/`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.error ||
            `${mediaType} upload failed.`
        );
      }

      // =================================================
      // BUILD MEDIA URL
      // =================================================

      const mediaUrl = data.file_url
        ? data.file_url.startsWith("http")
          ? data.file_url
          : `${API_URL}${data.file_url}`
        : null;

      if (!mediaUrl) {
        throw new Error(
          "Upload succeeded but the server did not return a file URL."
        );
      }

      // =================================================
      // DISPLAY MEDIA INSIDE CHAT
      // =================================================

      setMessages((previousMessages) => [
        ...previousMessages,
        {
          id: Date.now(),
          sender: "user",
          type: mediaType,
          text: file.name,
          mediaUrl: mediaUrl,
          fileName: file.name,
          fileSize: file.size,
          mimeType: file.type,
        },
      ]);

      console.log(
        `${mediaType} uploaded successfully:`,
        data
      );
    } catch (error) {
      console.error(
        "Media upload error:",
        error
      );

      setMessages((previousMessages) => [
        ...previousMessages,
        {
          id: Date.now(),
          sender: "bot",
          text: `${mediaType.charAt(0).toUpperCase() +
            mediaType.slice(1)} upload failed: ${
            error.message
          }`,
        },
      ]);
    } finally {
      setUploading(false);

      // Allows selecting the same file again
      event.target.value = "";
    }
  };

  // =====================================================
  // GET DIAGNOSIS
  // =====================================================

  const getDiagnosis = async () => {
    if (
      !conversationId ||
      loading ||
      uploading ||
      !canDiagnose ||
      diagnosisGenerated
    ) {
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(
        `${API_URL}/api/diagnosis/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            conversation_id: conversationId,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.error ||
            "Unable to generate diagnosis."
        );
      }

      // =================================================
      // NOT ENOUGH INFORMATION
      // =================================================

      if (!data.diagnosis_available) {
        setMessages((previousMessages) => [
          ...previousMessages,
          {
            id: Date.now(),
            sender: "bot",
            text: data.message,
          },
        ]);

        setCanDiagnose(false);

        return;
      }

      // =================================================
      // ADD DIAGNOSIS CARD
      // =================================================

      setMessages((previousMessages) => [
        ...previousMessages,
        {
          id: Date.now(),
          sender: "bot",
          type: "diagnosis",
          diagnosis: data,
        },
      ]);

      // Diagnosis has now been generated
      setDiagnosisGenerated(true);
      setCanDiagnose(false);
    } catch (error) {
      console.error(
        "Diagnosis API error:",
        error
      );

      setMessages((previousMessages) => [
        ...previousMessages,
        {
          id: Date.now(),
          sender: "bot",
          text: `Unable to generate diagnosis: ${error.message}`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  // =====================================================
  // BOOKING FORM HANDLER
  // =====================================================

  const handleBookingChange = (event) => {
    const { name, value } = event.target;

    setBookingForm((previousForm) => ({
      ...previousForm,
      [name]: value,
    }));
  };

  // =====================================================
  // OPEN BOOKING FORM
  // =====================================================

  const openBookingForm = () => {
    if (!conversationId) {
      alert(
        "Please start a conversation first."
      );

      return;
    }

    if (!diagnosisGenerated) {
      alert(
        "Please get a diagnosis before booking a mechanic."
      );

      return;
    }

    setBookingResult(null);

    setBookingForm((previousForm) => ({
      ...previousForm,
      service:
        previousForm.service ||
        "Vehicle inspection and repair",
    }));

    setShowBookingForm(true);
  };

  // =====================================================
  // CLOSE BOOKING FORM
  // =====================================================

  const closeBookingForm = () => {
    if (bookingLoading) {
      return;
    }

    setShowBookingForm(false);
  };

  // =====================================================
  // CREATE BOOKING
  // =====================================================

  const createBooking = async (event) => {
    event.preventDefault();

    if (bookingLoading) {
      return;
    }

    // =================================================
    // BASIC VALIDATION
    // =================================================

    if (
      !bookingForm.customer_name.trim() ||
      !bookingForm.phone.trim() ||
      !bookingForm.vehicle.trim() ||
      !bookingForm.service.trim() ||
      !bookingForm.preferred_date ||
      !bookingForm.preferred_time
    ) {
      alert(
        "Please fill in all booking fields."
      );

      return;
    }

    // =================================================
    // PHONE VALIDATION
    // =================================================

    const phonePattern =
      /^[0-9+\-\s()]{10,20}$/;

    if (
      !phonePattern.test(
        bookingForm.phone.trim()
      )
    ) {
      alert(
        "Please enter a valid phone number."
      );

      return;
    }

    setBookingLoading(true);

    try {
      const response = await fetch(
        `${API_URL}/api/booking/`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            customer_name:
              bookingForm.customer_name.trim(),

            phone:
              bookingForm.phone.trim(),

            vehicle:
              bookingForm.vehicle.trim(),

            service:
              bookingForm.service.trim(),

            preferred_date:
              bookingForm.preferred_date,

            preferred_time:
              bookingForm.preferred_time,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        console.error(
          "Booking API error:",
          data
        );

        // =================================================
        // HANDLE DRF VALIDATION ERRORS
        // =================================================

        let errorMessage =
          "Unable to create booking.";

        if (data.detail) {
          errorMessage = data.detail;
        } else if (data.error) {
          errorMessage = data.error;
        } else if (
          typeof data === "object"
        ) {
          const validationMessages = [];

          Object.entries(data).forEach(
            ([field, errors]) => {
              if (Array.isArray(errors)) {
                validationMessages.push(
                  `${field}: ${errors.join(", ")}`
                );
              } else if (
                typeof errors === "string"
              ) {
                validationMessages.push(
                  `${field}: ${errors}`
                );
              }
            }
          );

          if (
            validationMessages.length > 0
          ) {
            errorMessage =
              validationMessages.join("\n");
          }
        }

        throw new Error(errorMessage);
      }

      console.log(
        "Booking created:",
        data
      );

      setBookingResult(data);
    } catch (error) {
      console.error(
        "Booking error:",
        error
      );

      alert(
        `Booking failed: ${error.message}`
      );
    } finally {
      setBookingLoading(false);
    }
  };

  // =====================================================
  // RENDER MEDIA MESSAGE
  // =====================================================

  const renderMediaMessage = (message) => {
    // =================================================
    // IMAGE
    // =================================================

    if (message.type === "image") {
      return (
        <div className="image-message">
          <img
            src={message.mediaUrl}
            alt={message.fileName || "Uploaded car image"}
            className="uploaded-image"
          />

          <div className="image-name">
            {message.fileName || message.text}
          </div>
        </div>
      );
    }

    // =================================================
    // AUDIO
    // =================================================

    if (message.type === "audio") {
      return (
        <div className="media-message audio-message">
          <div className="media-icon">
            🎵
          </div>

          <div className="media-content">
            <div className="media-name">
              {message.fileName || message.text}
            </div>

            <audio
              controls
              preload="metadata"
              src={message.mediaUrl}
              className="uploaded-audio"
            >
              Your browser does not support
              audio playback.
            </audio>
          </div>
        </div>
      );
    }

    // =================================================
    // VIDEO
    // =================================================

    if (message.type === "video") {
      return (
        <div className="video-message">
          <video
            controls
            preload="metadata"
            src={message.mediaUrl}
            className="uploaded-video"
          >
            Your browser does not support
            video playback.
          </video>

          <div className="video-name">
            {message.fileName || message.text}
          </div>
        </div>
      );
    }

    return null;
  };

  // =====================================================
  // UI
  // =====================================================

  return (
    <div className="app">

      {/* =================================================
          HEADER
      ================================================= */}

      <header className="header">

        <div className="brand">

          <div className="brand-icon">
            🔧
          </div>

          <div>
            <h1>
              AI Car Mechanic
            </h1>

            <p>
              <span className="online-dot"></span>
              Online
            </p>
          </div>

        </div>

      </header>

      {/* =================================================
          CHAT
      ================================================= */}

      <main className="chat-container">

        <div className="messages">

          {messages.map((message) => (

            <div
              key={message.id}
              className={`message-row ${message.sender}`}
            >

              {/* BOT AVATAR */}

              {message.sender === "bot" && (
                <div className="avatar bot-avatar">
                  🤖
                </div>
              )}

              <div className="message-content">

                {/* =====================================
                    NORMAL MESSAGE
                ===================================== */}

                {!message.type && (
                  <div className="message-bubble">
                    {message.text}
                  </div>
                )}

                {/* =====================================
                    IMAGE / AUDIO / VIDEO
                ===================================== */}

                {[
                  "image",
                  "audio",
                  "video",
                ].includes(message.type) &&
                  renderMediaMessage(message)}

                {/* =====================================
                    DIAGNOSIS CARD
                ===================================== */}

                {message.type === "diagnosis" && (

                  <div className="diagnosis-card">

                    <div className="diagnosis-header">

                      <div className="diagnosis-icon">
                        🔍
                      </div>

                      <div>
                        <h3>
                          Vehicle Diagnosis
                        </h3>

                        <p>
                          Based on the information provided
                        </p>
                      </div>

                    </div>

                    {/* PROBLEM */}

                    <div className="diagnosis-section">

                      <span className="diagnosis-label">
                        Possible Problem
                      </span>

                      <p>
                        {message.diagnosis.problem}
                      </p>

                    </div>

                    {/* EXPLANATION */}

                    <div className="diagnosis-section">

                      <span className="diagnosis-label">
                        Explanation
                      </span>

                      <p>
                        {message.diagnosis.explanation}
                      </p>

                    </div>

                    {/* SEVERITY */}

                    <div className="diagnosis-section">

                      <span className="diagnosis-label">
                        Severity
                      </span>

                      <span
                        className={`severity-badge ${
                          String(
                            message.diagnosis.severity ||
                              ""
                          ).toLowerCase()
                        }`}
                      >
                        {String(
                          message.diagnosis.severity ||
                            "Unknown"
                        ).toUpperCase()}
                      </span>

                    </div>

                    {/* RECOMMENDATION */}

                    <div className="diagnosis-section">

                      <span className="diagnosis-label">
                        Recommendation
                      </span>

                      <p>
                        {message.diagnosis.recommendation}
                      </p>

                    </div>

                  </div>

                )}

              </div>

              {/* USER AVATAR */}

              {message.sender === "user" && (
                <div className="avatar user-avatar">
                  👤
                </div>
              )}

            </div>

          ))}

          {/* =================================================
              CHAT LOADING
          ================================================= */}

          {loading && (

            <div className="message-row bot">

              <div className="avatar bot-avatar">
                🤖
              </div>

              <div className="message-content">

                <div className="message-bubble typing">
                  Mechanic is thinking...
                </div>

              </div>

            </div>

          )}

          {/* =================================================
              UPLOAD LOADING
          ================================================= */}

          {uploading && (

            <div className="message-row bot">

              <div className="avatar bot-avatar">
                🤖
              </div>

              <div className="message-content">

                <div className="message-bubble typing">
                  Uploading your media...
                </div>

              </div>

            </div>

          )}

        </div>

      </main>

      {/* =================================================
          INPUT AREA
      ================================================= */}

      <div className="input-area">

        <div className="input-wrapper">

          {/* =================================================
              HIDDEN FILE INPUT

              Supports:
              IMAGE
              AUDIO
              VIDEO
          ================================================= */}

          <input
            ref={fileInputRef}
            type="file"
            accept="image/*,audio/*,video/*"
            onChange={handleFileChange}
            className="hidden-file-input"
          />

          {/* =================================================
              ATTACHMENT BUTTON
          ================================================= */}

          <button
            className="attachment-button"
            type="button"
            onClick={openFileSelector}
            disabled={
              loading ||
              uploading ||
              diagnosisGenerated
            }
            title="Upload image, audio, or video"
          >
            📎
          </button>

          {/* =================================================
              TEXT INPUT
          ================================================= */}

          <textarea
            value={input}
            onChange={(event) =>
              setInput(event.target.value)
            }
            onKeyDown={handleKeyDown}
            placeholder={
              diagnosisGenerated
                ? "Diagnosis completed"
                : "Describe your car problem..."
            }
            rows="1"
            disabled={
              loading ||
              uploading ||
              diagnosisGenerated
            }
          />

          {/* =================================================
              SEND
          ================================================= */}

          <button
            className="send-button"
            type="button"
            onClick={sendMessage}
            disabled={
              !input.trim() ||
              loading ||
              uploading ||
              diagnosisGenerated
            }
          >
            ➤
          </button>

        </div>

        <p className="input-hint">
          Press Enter to send • Shift + Enter for a new line
          • 📎 Image / Audio / Video
        </p>

      </div>

      {/* =================================================
          ACTION BUTTONS
      ================================================= */}

      <div className="booking-area">

        {/* GET DIAGNOSIS */}

        <button
          className="diagnosis-button"
          type="button"
          onClick={getDiagnosis}
          disabled={
            !conversationId ||
            !canDiagnose ||
            diagnosisGenerated ||
            loading ||
            uploading
          }
        >
          {diagnosisGenerated
            ? "✓ Diagnosis Complete"
            : "🔍 Get Diagnosis"}
        </button>

        {/* BOOK MECHANIC */}

        <button
          className="booking-button"
          type="button"
          onClick={openBookingForm}
          disabled={
            !conversationId ||
            !diagnosisGenerated
          }
        >
          🔧 Book a Mechanic
        </button>

      </div>

      {/* =================================================
          BOOKING MODAL
      ================================================= */}

      {showBookingForm && (

        <div
          className="booking-modal-overlay"
          onMouseDown={(event) => {

            if (
              event.target ===
              event.currentTarget
            ) {
              closeBookingForm();
            }

          }}
        >

          <div className="booking-modal">

            {/* =================================================
                BOOKING FORM
            ================================================= */}

            {!bookingResult ? (

              <>

                {/* MODAL HEADER */}

                <div className="booking-modal-header">

                  <div>

                    <h2>
                      Book a Mechanic
                    </h2>

                    <p>
                      Schedule a mechanic for your vehicle.
                    </p>

                  </div>

                  <button
                    type="button"
                    className="booking-close-button"
                    onClick={closeBookingForm}
                    disabled={bookingLoading}
                  >
                    ✕
                  </button>

                </div>

                {/* FORM */}

                <form
                  className="booking-form"
                  onSubmit={createBooking}
                >

                  {/* CUSTOMER NAME */}

                  <div className="form-group">

                    <label htmlFor="customer_name">
                      Your Name
                    </label>

                    <input
                      id="customer_name"
                      name="customer_name"
                      type="text"
                      placeholder="Enter your name"
                      value={
                        bookingForm.customer_name
                      }
                      onChange={
                        handleBookingChange
                      }
                      disabled={bookingLoading}
                      autoComplete="name"
                      required
                    />

                  </div>

                  {/* PHONE */}

                  <div className="form-group">

                    <label htmlFor="phone">
                      Phone Number
                    </label>

                    <input
                      id="phone"
                      name="phone"
                      type="tel"
                      placeholder="Enter your phone number"
                      value={
                        bookingForm.phone
                      }
                      onChange={
                        handleBookingChange
                      }
                      disabled={bookingLoading}
                      autoComplete="tel"
                      required
                    />

                  </div>

                  {/* VEHICLE */}

                  <div className="form-group">

                    <label htmlFor="vehicle">
                      Vehicle
                    </label>

                    <input
                      id="vehicle"
                      name="vehicle"
                      type="text"
                      placeholder="Example: Hyundai Creta 2022"
                      value={
                        bookingForm.vehicle
                      }
                      onChange={
                        handleBookingChange
                      }
                      disabled={bookingLoading}
                      required
                    />

                  </div>

                  {/* SERVICE */}

                  <div className="form-group">

                    <label htmlFor="service">
                      Service Required
                    </label>

                    <input
                      id="service"
                      name="service"
                      type="text"
                      placeholder="Example: Brake inspection"
                      value={
                        bookingForm.service
                      }
                      onChange={
                        handleBookingChange
                      }
                      disabled={bookingLoading}
                      required
                    />

                  </div>

                  {/* DATE + TIME */}

                  <div className="booking-row">

                    <div className="form-group">

                      <label htmlFor="preferred_date">
                        Preferred Date
                      </label>

                      <input
                        id="preferred_date"
                        name="preferred_date"
                        type="date"
                        value={
                          bookingForm.preferred_date
                        }
                        onChange={
                          handleBookingChange
                        }
                        disabled={bookingLoading}
                        min={
                          new Date()
                            .toISOString()
                            .split("T")[0]
                        }
                        required
                      />

                    </div>

                    <div className="form-group">

                      <label htmlFor="preferred_time">
                        Preferred Time
                      </label>

                      <input
                        id="preferred_time"
                        name="preferred_time"
                        type="time"
                        value={
                          bookingForm.preferred_time
                        }
                        onChange={
                          handleBookingChange
                        }
                        disabled={bookingLoading}
                        required
                      />

                    </div>

                  </div>

                  {/* ACTION BUTTONS */}

                  <div className="booking-form-actions">

                    <button
                      type="button"
                      className="booking-cancel-button"
                      onClick={closeBookingForm}
                      disabled={bookingLoading}
                    >
                      Cancel
                    </button>

                    <button
                      type="submit"
                      className="booking-submit-button"
                      disabled={bookingLoading}
                    >
                      {bookingLoading
                        ? "Booking..."
                        : "✓ Confirm Booking"}
                    </button>

                  </div>

                </form>

              </>

            ) : (

              /* =================================================
                 BOOKING SUCCESS
              ================================================= */

              <div className="booking-success">

                <div className="booking-success-icon">
                  ✓
                </div>

                <h2>
                  Booking Request Created
                </h2>

                <p>
                  Your mechanic booking has been
                  submitted successfully.
                </p>

                <div className="booking-details">

                  {/* BOOKING ID */}

                  <div className="booking-detail">

                    <span>
                      Booking ID
                    </span>

                    <strong>
                      #
                      {bookingResult.booking_id ||
                        bookingResult.booking?.id ||
                        "N/A"}
                    </strong>

                  </div>

                  {/* STATUS */}

                  <div className="booking-detail">

                    <span>
                      Status
                    </span>

                    <strong className="booking-status">
                      {String(
                        bookingResult.status ||
                          bookingResult.booking?.status ||
                          "pending"
                      ).toUpperCase()}
                    </strong>

                  </div>

                  {/* VEHICLE */}

                  <div className="booking-detail">

                    <span>
                      Vehicle
                    </span>

                    <strong>
                      {bookingForm.vehicle}
                    </strong>

                  </div>

                  {/* SERVICE */}

                  <div className="booking-detail">

                    <span>
                      Service
                    </span>

                    <strong>
                      {bookingForm.service}
                    </strong>

                  </div>

                  {/* DATE */}

                  <div className="booking-detail">

                    <span>
                      Date
                    </span>

                    <strong>
                      {bookingForm.preferred_date}
                    </strong>

                  </div>

                  {/* TIME */}

                  <div className="booking-detail">

                    <span>
                      Time
                    </span>

                    <strong>
                      {bookingForm.preferred_time}
                    </strong>

                  </div>

                </div>

                {/* DONE */}

                <button
                  type="button"
                  className="booking-done-button"
                  onClick={() => {
                    setShowBookingForm(false);
                    setBookingResult(null);
                  }}
                >
                  Done
                </button>

              </div>

            )}

          </div>

        </div>

      )}

    </div>
  );
}

export default App;