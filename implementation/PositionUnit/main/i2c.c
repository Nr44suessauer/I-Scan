#include "include/i2c.h"


/**
 * @brief Initializes the I2C master interface.
 *
 * This function sets up the I2C master interface for communication with I2C slave devices.
 * It configures the necessary hardware registers and settings to enable I2C communication.
 *
 * @note This function must be called before any I2C communication can take place.
 */
esp_err_t i2c_master_init(void)
{
    i2c_config_t conf = {
        .mode = I2C_MODE_MASTER,
        .sda_io_num = I2C_MASTER_SDA_IO,
        .sda_pullup_en = GPIO_PULLUP_ENABLE,
        .scl_io_num = I2C_MASTER_SCL_IO,
        .scl_pullup_en = GPIO_PULLUP_ENABLE,
        .master.clk_speed = I2C_MASTER_FREQ_HZ,
    };
    i2c_param_config(I2C_MASTER_NUM, &conf);
    return i2c_driver_install(I2C_MASTER_NUM, conf.mode,
                              I2C_MASTER_RX_BUF_DISABLE,
                              I2C_MASTER_TX_BUF_DISABLE, 0);
}

/**
 * @brief Write data to an I2C slave device.
 *
 * This function sends data to a specified I2C slave device. It initiates
 * a write operation by sending the slave address followed by the data bytes.
 * The function ensures that the data is transmitted correctly by checking
 * the acknowledgment from the slave device.
 *
 * @param i2c_num I2C port number to use for the operation.
 * @param slave_addr Address of the I2C slave device.
 * @param data Pointer to the data buffer to be sent.
 * @param data_len Length of the data buffer.
 * @param timeout Maximum time to wait for the operation to complete.
 *
 * @return
 *     - ESP_OK: Success
 *     - ESP_ERR_INVALID_ARG: Parameter error
 *     - ESP_FAIL: Sending command error, slave doesn't acknowledge the transfer.
 */
esp_err_t i2c_master_write_slave(uint8_t* data, size_t data_len)
{
    i2c_cmd_handle_t cmd = i2c_cmd_link_create();
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (I2C_SLAVE_ADDR << 1) | I2C_MASTER_WRITE, true);
    i2c_master_write(cmd, data, data_len, true);
    i2c_master_stop(cmd);
    esp_err_t ret = i2c_master_cmd_begin(I2C_MASTER_NUM, cmd, I2C_MASTER_TIMEOUT_MS / portTICK_PERIOD_MS);
    i2c_cmd_link_delete(cmd);
    return ret;
}

/**
 * @brief Reads data from an I2C slave device.
 *
 * This function initiates a read operation from a specified I2C slave device.
 * It sends the slave address along with the read bit, and then reads the
 * specified number of bytes from the slave device into the provided buffer.
 *
 * @param i2c_num I2C port number to use for the read operation.
 * @param data_rd Pointer to the buffer where the read data will be stored.
 * @param size Number of bytes to read from the slave device.
 *
 * @return
 *     - ESP_OK: Success
 *     - ESP_ERR_INVALID_ARG: Parameter error
 *     - ESP_FAIL: Sending command error, slave doesn't ACK the transfer.
 */
esp_err_t i2c_master_read_slave(uint8_t* data, size_t data_len)
{
    i2c_cmd_handle_t cmd = i2c_cmd_link_create();
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (I2C_SLAVE_ADDR << 1) | I2C_MASTER_READ, true);
    i2c_master_read(cmd, data, data_len, I2C_MASTER_LAST_NACK);
    i2c_master_stop(cmd);
    esp_err_t ret = i2c_master_cmd_begin(I2C_MASTER_NUM, cmd, I2C_MASTER_TIMEOUT_MS / portTICK_PERIOD_MS);
    i2c_cmd_link_delete(cmd);
    return ret;
}

/**
 * @brief Checks if a slave device is present on the I2C bus.
 *
 * This function sends a write command to the specified I2C address to check if a slave device
 * is present on the bus. It returns a status indicating whether the device acknowledged the
 * command or not.
 *
 * @param I2C_MASTER_NUM I2C port number to use for the check (MASTER OUTPUT).
 * @param I2C_SLAVE_ADDR I2C address of the slave device to check.
 * @return
 *     - ESP_OK if the slave device is present and acknowledged the command.
 *     - ESP_ERR_INVALID_ARG if the arguments are invalid.
 *     - ESP_FAIL if the slave device did not acknowledge the command.
 */
esp_err_t i2c_master_check_slave(void)
{
    i2c_cmd_handle_t cmd = i2c_cmd_link_create();
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (I2C_SLAVE_ADDR << 1) | I2C_MASTER_WRITE, true);
    i2c_master_stop(cmd);
    esp_err_t ret = i2c_master_cmd_begin(I2C_MASTER_NUM, cmd, I2C_MASTER_TIMEOUT_MS / portTICK_PERIOD_MS);
    i2c_cmd_link_delete(cmd);

    if (ret == ESP_OK) {
        printf("I2C Slave connection is OK.\n");
    } else {
        printf("I2C Slave connection failed.\n");
    }

    return ret;
}

/**
 * @brief Read data from a specific register of an I2C slave device.
 *
 * This function writes the register address to the I2C slave device and then reads the data from that register.
 *
 * @param reg_addr The address of the register to read from.
 * @param data Pointer to the buffer where the read data will be stored.
 * @param data_len The length of the data to be read.
 * 
 * @return
 *     - ESP_OK: Success
 *     - ESP_ERR_INVALID_ARG: Parameter error
 *     - ESP_FAIL: Sending command error, slave doesn't ACK the transfer.
 *     - ESP_ERR_INVALID_STATE: I2C driver not installed or not in master mode.
 *     - ESP_ERR_TIMEOUT: Operation timeout because the bus is busy.
 */

esp_err_t i2c_master_read_register(uint8_t reg_addr, uint8_t* data, size_t data_len)
{
    esp_err_t ret;
    ret = i2c_master_write_slave(&reg_addr, 1);
    if (ret != ESP_OK) {
        return ret;
    }
    return i2c_master_read_slave(data, data_len);
}

/**
 * @brief Scans the I2C bus for connected devices.
 *
 * This function scans the I2C bus for devices by sending a write command to each possible
 * address (from 1 to 126). If a device acknowledges the command, its address is printed
 * to the console.
 *
 * The function uses the ESP-IDF I2C master driver to create and execute I2C commands.
 * It prints the address of each detected device in hexadecimal format.
 *
 * @note This function assumes that the I2C master driver has been initialized and configured
 *       before calling this function.
 */

void i2c_scanner(void)
{
    printf("Scanning I2C bus...\n");
    for (uint8_t addr = 1; addr < 127; addr++) {
        i2c_cmd_handle_t cmd = i2c_cmd_link_create();
        i2c_master_start(cmd);
        i2c_master_write_byte(cmd, (addr << 1) | I2C_MASTER_WRITE, true);
        i2c_master_stop(cmd);
        esp_err_t ret = i2c_master_cmd_begin(I2C_MASTER_NUM, cmd, I2C_MASTER_TIMEOUT_MS / portTICK_PERIOD_MS);
        i2c_cmd_link_delete(cmd);

        if (ret == ESP_OK) {
            printf("Found device at address 0x%02x\n", addr);
        }
    }
    printf("I2C scan completed.\n");
}

/**
 * @brief Reads the distance value from an I2C device.
 *
 * This function reads two bytes from an I2C device to calculate the distance.
 * It reads the high byte from register 0x01 and the low byte from register 0x00.
 * The two bytes are then combined to form a 16-bit distance value.
 *
 * @return uint16_t The 16-bit distance value read from the I2C device.
 *
 * The function performs the following steps:
 * 1. Declares two 8-bit variables, HighByte and LowByte, to store the high and low bytes read from the I2C device.
 * 2. Reads the high byte from register 0x01 using the i2c_master_read_register function and stores it in HighByte.
 * 3. Reads the low byte from register 0x00 using the i2c_master_read_register function and stores it in LowByte.
 * 4. Combines the high and low bytes to form a 16-bit value by shifting HighByte 8 bits to the left and performing a bitwise OR with LowByte.
 * 5. Returns the combined 16-bit distance value.
 */
uint16_t distance_read()
{      
    uint8_t HighByte;
    uint8_t LowByte; 

    i2c_master_read_register(0x01, &HighByte, 1);
    printf("Value HIGH: %d\n", HighByte);

    i2c_master_read_register(0x00, &LowByte, 1);
    printf("Value LOW: %d\n",LowByte);

    uint16_t ret = (HighByte << 8) | LowByte;
    // printf("Value: %d\n", myVariable);
    return ret;
        
}