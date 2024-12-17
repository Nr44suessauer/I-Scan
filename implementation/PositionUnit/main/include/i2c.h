#ifndef I2C_H
#define I2C_H

#include "driver/i2c.h"
// API Documentation: https://docs.espressif.com/projects/esp-idf/en/stable/esp32c6/api-reference/peripherals/i2c.html

#define I2C_MASTER_SCL_IO           11    /*!< GPIO number for I2C master clock */
#define I2C_MASTER_SDA_IO           10    /*!< GPIO number for I2C master data */
#define I2C_MASTER_NUM              I2C_NUM_0 /*!< I2C port number for master device */
#define I2C_MASTER_FREQ_HZ          100000     /*!< I2C master clock frequency */
#define I2C_MASTER_TX_BUF_DISABLE   0          /*!< Disable I2C master TX buffer */
#define I2C_MASTER_RX_BUF_DISABLE   0          /*!< Disable I2C master RX buffer */
#define I2C_MASTER_TIMEOUT_MS       1000       /*!< I2C operation timeout in milliseconds */

#define TF_LUNA                     0x10 /*!< I2C slave address */

/**
 * @brief Initialize the I2C master interface.
 *
 * Configures and installs the I2C driver for master operations.
 *
 * @return
 *     - ESP_OK on success
 *     - ESP_ERR_INVALID_ARG on invalid parameters
 *     - Other ESP errors on failure
 */
esp_err_t i2c_master_init(void);

/**
 * @brief Write data to an I2C slave device.
 *
 * Sends a sequence of bytes to the specified slave address.
 *
 * @param data Pointer to the data buffer to send.
 * @param data_len Number of bytes to write.
 *
 * @return
 *     - ESP_OK on success
 *     - ESP_ERR_INVALID_ARG on invalid parameters
 *     - ESP_FAIL if the slave does not acknowledge
 */
esp_err_t i2c_master_write_slave(uint8_t* data, size_t data_len);

/**
 * @brief Check the presence of an I2C slave device.
 *
 * Verifies if a slave device acknowledges its address on the I2C bus.
 *
 * @return
 *     - ESP_OK if the slave is present
 *     - ESP_ERR_INVALID_ARG on invalid parameters
 *     - ESP_FAIL if the slave does not acknowledge
 */
esp_err_t i2c_master_check_slave(void);

/**
 * @brief Read data from an I2C slave device.
 *
 * Retrieves a sequence of bytes from the specified slave address.
 *
 * @param data Pointer to the buffer to store read data.
 * @param data_len Number of bytes to read.
 *
 * @return
 *     - ESP_OK on success
 *     - ESP_ERR_INVALID_ARG on invalid parameters
 *     - ESP_FAIL if the slave does not acknowledge
 */
esp_err_t i2c_master_read_slave(uint8_t* data, size_t data_len);

/**
 * @brief Read a specific register from an I2C slave device.
 *
 * Reads data from a designated register address of the slave device.
 *
 * @param reg_addr Register address to read from.
 * @param data Pointer to the buffer to store read data.
 * @param data_len Number of bytes to read.
 *
 * @return
 *     - ESP_OK on success
 *     - ESP_ERR_INVALID_ARG on invalid parameters
 *     - ESP_FAIL if the slave does not acknowledge
 *     - ESP_ERR_INVALID_STATE if the driver is not initialized
 *     - ESP_ERR_TIMEOUT on operation timeout
 */
esp_err_t i2c_master_read_register(uint8_t reg_addr, uint8_t* data, size_t data_len);

/**
 * @brief Scan the I2C bus for connected devices.
 *
 * Iterates through possible I2C addresses and reports devices that acknowledge.
 */
void i2c_scanner(void);

/**
 * @brief Read the distance value from the I2C device.
 *
 * Combines high and low bytes from specific registers to calculate the distance.
 *
 * @return 16-bit distance value.
 */
uint16_t distance_read();

#endif // I2C_H
