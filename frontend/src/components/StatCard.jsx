import React from "react";
import { Card, CardContent, Typography, Box } from "@mui/material";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

// Register chart components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const StatCard = ({ title, value, subtitle, icon, backgroundColor }) => {
  return (
    <Card
      sx={{
        borderRadius: 4,
        boxShadow: 3,
        width: "100%",
        backgroundColor: backgroundColor,
        color: "#fff",
        px: { xs: 2, sm: 3 },
        py: { xs: 2, sm: 2.5 },
      }}
    >
      <CardContent sx={{ padding: 0, "&:last-child": { paddingBottom: 0 } }}>
        <Box
          display="flex"
          flexDirection={{ xs: "column", sm: "row" }}
          alignItems={{ xs: "flex-start", sm: "center" }}
        >
          <Box
            sx={{
              width: 50,
              height: 50,
              backgroundColor: "#2f527a4d",
              borderRadius: 2,
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              mb: { xs: 1.5, sm: 0 },
            }}
          >
            <Box
              component="span"
              sx={{
                fontSize: 24,
                color: "#2f527a",
              }}
            >
              {icon}
            </Box>
          </Box>

          {/* Title & Value Section with Fixed Height */}
          <Box
            ml={{ xs: 0, sm: 2 }}
            sx={{
              minHeight: 80,
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
            }}
          >
            <Typography
              variant="body2"
              sx={{
                fontSize: { xs: "0.85rem", sm: "0.875rem" },
                color: "#2f527a",
                textAlign: "left",
                lineHeight: 1,
              }}
            >
              {title}
            </Typography>
            <Typography
              variant="h5"
              fontWeight="bold"
              sx={{
                fontSize: { xs: "1.25rem", sm: "1.5rem" },
                color: "#2f527a",
                textAlign: "left",
                lineHeight: 1.5,
              }}
            >
              {value}
            </Typography>
          </Box>
        </Box>

        <Box mt={1} display="flex" alignItems="center">
          <Typography
            variant="body2"
            sx={{
              fontSize: "0.875rem",
              color: "#2f527a",
              textAlign: "left",
              lineHeight: 1.3,
            }}
          >
            {subtitle}
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};

export default StatCard;
