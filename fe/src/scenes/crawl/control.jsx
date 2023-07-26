import axios from "axios";
import React, { useEffect, useState } from "react";
import {
  Box,
  Button,
  Grid,
  TextField,
  useTheme,
  Modal,
  Typography,
} from "@mui/material";
import Header from "components/Header";
import { ToastContainer, toast } from "react-toastify";
import { API_BASE_URL } from "scenes/api/api";


function Search() {
  const authToken = JSON.parse(JSON.stringify(localStorage.getItem("token")));
  const theme = useTheme();
  const [loading, setLoading] = useState(false);
  const [isTime, setIsTime] = useState(false);
  const [number, setNumber] = useState(8);
  const [time, setTime] = useState("");


  
  useEffect(() => {
    getStatus();
  }, [isTime]);

  const getStatus = async () => {
    try {
      const response = await axios.get(API_BASE_URL + "/job-exist", {
        headers: {
          Authorization: `Bearer ${authToken}`,
        },
      });
      console.log(response.data.status);
      if (response.data.message === "on") {
        setLoading(true);
        setTime(response.data.next_time);
      } else {
        setTime("");
        setLoading(false);
        setNumber(8);
      }
    } catch (error) {
      console.error("Lỗi khi gửi yêu cầu:", error);
    }
  };

  const handleChange = (e) => {
    const value = e.target.value;
    if (value === "") {
      setNumber("");
    } else if (/^\d+$/.test(value) && parseInt(value) > 0) {
      setNumber(value);
    }
  };
  const handleSubmit = async (e) => {
    setLoading(true);
    e.preventDefault();
    setOpenModal(false);
    try {
      const status = "true";
      const quantity = parseInt(number);
      const unit = "hour";
      const name = "cronjob"
      const response = await axios.post(
        API_BASE_URL + "/cron-job",
        {
          status,
          quantity,
          unit,
          name
        },
        {
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        }
      );
      setIsTime(!isTime);
      console.log("Yêu cầu đã được gửi thành công!");
      if (response.data.status === "success") {
        toast.success("Tự động Crawl đã được bật", {
          position: toast.POSITION.TOP_CENTER,
          autoClose: 3000,
          hideProgressBar: true,
        });
      }
    } catch (error) {
      console.error("Lỗi khi gửi yêu cầu:", error);
    }
  };

  const [open, setOpen] = useState(false);
  const [openModal, setOpenModal] = useState(false);

  const handleModal = async () => {
    setOpen(true);
  };

  const handleModalSubmit = async () => {
    setOpenModal(true);
  };

  const handleCancelModal = async () => {
    setOpenModal(false);
  };

  const handleCancel = async () => {
    setOpen(false);
  };
  const handleClose = () => {
    setOpen(false);
  };

  const handleConfirm = async () => {
    setOpen(false);
    try {
      const status = "false";
      const quantity = parseInt(number);
      const unit = "hour";
      const name = "cronjob"
      const response = await axios.post(
        API_BASE_URL + "/cron-job",
        {
          status,
          quantity,
          unit,
          name
        },
        {
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        }
      );
      console.log(response.data);
      if (response.data.status === "success") {
        toast.success("Tự động Crawl đã được tắt", {
          position: toast.POSITION.TOP_CENTER,
          autoClose: 3000,
          hideProgressBar: true,
        });
      }
    } catch (error) {}
    setLoading(false);
    setTime("")
  };

  return (
    <>
      <Box m="1.5rem 2.5rem">
        <ToastContainer />
        <Header title="Crawl Setting" />
        <Box
          mt="40px"
          height="75vh"
          sx={{
            "& .MuiDataGrid-root": {
              border: "none",
            },
            "& .MuiDataGrid-cell": {
              borderBottom: "none",
            },
            "& .MuiDataGrid-columnHeaders": {
              backgroundColor: theme.palette.background.alt,
              color: theme.palette.secondary[100],
              borderBottom: "none",
            },
            "& .MuiDataGrid-virtualScroller": {
              backgroundColor: theme.palette.primary.light,
            },
            "& .MuiDataGrid-footerContainer": {
              backgroundColor: theme.palette.background.alt,
              color: theme.palette.secondary[100],
              borderTop: "none",
            },
            "& .MuiDataGrid-toolbarContainer .MuiButton-text": {
              color: `${theme.palette.secondary[200]} !important`,
            },
            "& .image": {
              borderRadius: "50%",
            },
            "& .MuiDataGrid-checkboxInput.Mui-checked": {
              color: "white",
            },
            "& .css-1u3bzj6-MuiFormControl-root-MuiTextField-root": {
              marginRight: "10px",
            },
            "& .css-v3zyv7-MuiSelect-select-MuiInputBase-input-MuiOutlinedInput-input":
              {
                width: "80px",
              },
            "& .css-3cyd2n": {
              width: "100%",
            },
            "& .css-kg2jkk-MuiDataGrid-root": {
              maxWidth: "1189.2px",
              maxHeight: "559.2px",
            },
            "& .css-1vgpi90-MuiFormControl-root": {
              minWidth: "150px"
            },
          }}
        >
          <Grid item xs={10} sm={8} md={6} lg={4}>
            <Box sx={{ mb: 3 }}>
              <TextField
                style={{ width: "160px" }}
                label="Hour"
                name="hour"
                value={number}
                onChange={handleChange}
                variant="outlined"
                size="small"
                disabled={true}
              />
            </Box>
            <h4>Next time : {time}</h4>
            <Box sx={{ mb: 3 }}>
              <Button
                variant="contained"
                color="primary"
                onClick={handleModal}
                disabled={!loading}
              >
                OFF
              </Button>
              <Button
                variant="contained"
                color="primary"
                onClick={handleModalSubmit}
                sx={{ ml: 2 }}
                disabled={loading}
              >
                ON
              </Button>
            </Box>
          </Grid>
          <Modal open={open} onClose={handleClose}>
            <Box
              sx={{
                position: "absolute",
                top: "50%",
                left: "50%",
                transform: "translate(-50%, -50%)",
                width: 400,
                bgcolor: theme.palette.primary[700],
                borderRadius: 8,
                boxShadow: "0 2px 4px rgba(0, 0, 0, 0.2)",
                p: 4,
                textAlign: "center",
              }}
            >
              <Typography variant="h6" component="h2" sx={{ mb: 2 }}>
                Xác nhận để huỷ bỏ
              </Typography>
              <Typography variant="body1" component="p" sx={{ mb: 4 }}>
                Bạn có chắc chắn muốn tắt tự động lấy dữ liệu ?
              </Typography>
              <Box sx={{ display: "flex", justifyContent: "center" }}>
                <Button
                  variant="contained"
                  color="error"
                  onClick={handleCancel}
                  sx={{ mr: 2 }}
                >
                  Cancel
                </Button>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleConfirm}
                >
                  Confirm
                </Button>
              </Box>
            </Box>
          </Modal>
          <Modal open={openModal} onClose={handleClose}>
            <Box
              sx={{
                position: "absolute",
                top: "50%",
                left: "50%",
                transform: "translate(-50%, -50%)",
                width: 400,
                bgcolor: theme.palette.primary[700],
                borderRadius: 8,
                boxShadow: "0 2px 4px rgba(0, 0, 0, 0.2)",
                p: 4,
                textAlign: "center",
              }}
            >
              <Typography variant="h6" component="h2" sx={{ mb: 2 }}>
                Xác nhận để bật tự động lấy dữ liệu
              </Typography>
              <Typography variant="body1" component="p" sx={{ mb: 4 }}>
                Bạn có chắc muốn tự động lấy dữ liệu?
              </Typography>
              <Box sx={{ display: "flex", justifyContent: "center" }}>
                <Button
                  variant="contained"
                  color="error"
                  onClick={handleCancelModal}
                  sx={{ mr: 2 }}
                >
                  Cancel
                </Button>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleSubmit}
                >
                  Confirm
                </Button>
              </Box>
            </Box>
          </Modal>
        </Box>
      </Box>
    </>
  );
}

export default Search;
