const checkToken = () => {
    let tokenData = "";
    try {
      const { token } = JSON.parse(localStorage.getItem("user"));
      tokenData = `Token ${token}`;
    } catch {
      tokenData = "";
    }
    return tokenData;
  };
  
  const handleData = async (url, config) => {
    const response = await fetch(url, config);
    const json = await response.json();
    return [json, response.status];
  };
  
  export const deleteData = async (url) => {
    const tokenData = checkToken();
    return await handleData(url, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: tokenData,
      },
    });
  };
  
  export const fetchData = async (url) => {
    const tokenData = checkToken();
    return await handleData(url, {
      headers: { Authorization: tokenData },
    });
  };
  
  export const postData = async (url, data) => {
    const tokenData = checkToken();
    return await handleData(url, {
      credentials: 'include',
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: tokenData,
      },
      body: JSON.stringify(data),
    });
  };
  
  export const putData = async (url, data) => {
    const tokenData = checkToken();
    return await handleData(url, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: tokenData,
      },
      body: JSON.stringify(data),
    });
  };
  
  export const postFormData = async (url, data) => {
    const tokenData = checkToken();
    return await handleData(url, {
      method: "POST",
      headers: { Authorization: tokenData },
      body: data,
    });
  };
  
  export const putFormData = async (url, data) => {
    const tokenData = checkToken();
    const response = await fetch(url, {
      method: "PUT",
      headers: { Authorization: tokenData },
      body: data,
    });
    const json = await response.json();
    return json;
  };