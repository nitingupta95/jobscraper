import express from "express";
import scrapeRouter from "./routes";

const app = express();

app.use(express.json());
app.use("/api", scrapeRouter);

const PORT = 4000;
app.listen(PORT, () => {
  console.log(`🚀 Express running on http://localhost:${PORT}`);
});
