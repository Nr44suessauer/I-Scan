#include "include/i2c.h"


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

esp_err_t i2c_master_read_register(uint8_t reg_addr, uint8_t* data, size_t data_len)
{
    esp_err_t ret;
    ret = i2c_master_write_slave(&reg_addr, 1);
    if (ret != ESP_OK) {
        return ret;
    }
    return i2c_master_read_slave(data, data_len);
}

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
 * 2. Declares two pointers, HighByteValue and LowByteValue, to point to the addresses of HighByte and LowByte respectively.
 * 3. Reads the high byte from register 0x01 using the i2c_master_read_register function and stores it in HighByte.
 * 4. Prints the value of HighByte for debugging purposes.
 * 5. Reads the low byte from register 0x00 using the i2c_master_read_register function and stores it in LowByte.
 * 6. Prints the value of LowByte for debugging purposes.
 * 7. Combines the high and low bytes to form a 16-bit value by shifting HighByte 8 bits to the left and performing a bitwise OR with LowByte.
 * 8. Returns the combined 16-bit distance value.
 */
uint16_t distance_read()
{      
    uint8_t HighByte;
    uint8_t LowByte;

    uint16_t *HighByteValue = &HighByte;
    uint16_t *LowByteValue = &LowByte;  

    i2c_master_read_register(0x01, &HighByte, 1);
    printf("Value HIGH: %d\n", HighByte);

    i2c_master_read_register(0x00, &LowByte, 1);
    printf("Value LOW: %d\n",LowByte);

    uint16_t ret = (HighByte << 8) | LowByte;
    // printf("Value: %d\n", myVariable);
    return ret;
        
}