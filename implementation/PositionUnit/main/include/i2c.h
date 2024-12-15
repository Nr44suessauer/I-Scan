#ifndef I2C_H
#define I2C_H

#include "driver/i2c.h"
// API DOKU : https://docs.espressif.com/projects/esp-idf/en/stable/esp32c6/api-reference/peripherals/i2c.html




#define I2C_MASTER_SCL_IO           11    /*!< gpio number for I2C master clock */
#define I2C_MASTER_SDA_IO           10    /*!< gpio number for I2C master data  */
#define I2C_MASTER_NUM              I2C_NUM_0 /*!< I2C port number for master dev */
#define I2C_MASTER_FREQ_HZ          100000     /*!< I2C master clock frequency */
#define I2C_MASTER_TX_BUF_DISABLE   0    /*!< I2C master doesn't need buffer */
#define I2C_MASTER_RX_BUF_DISABLE   0    /*!< I2C master doesn't need buffer */
#define I2C_MASTER_TIMEOUT_MS       1000

#define I2C_SLAVE_ADDR              0x10 /*!< I2C slave address */


esp_err_t i2c_master_init(void);

esp_err_t i2c_master_write_slave(uint8_t* data, size_t data_len);

esp_err_t i2c_master_check_slave(void);

esp_err_t i2c_master_read_slave(uint8_t* data, size_t data_len);

uint16_t distance_read();

void i2c_scanner(void);

esp_err_t i2c_master_read_register(uint8_t reg_addr, uint8_t* data, size_t data_len);



#endif // I2C_H
