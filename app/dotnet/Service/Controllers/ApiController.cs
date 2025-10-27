using Microsoft.AspNetCore.Mvc;

namespace Service.Controllers;

[ApiController]
[Route("[controller]")]
public class ApiController : ControllerBase
{
    // GET /api
    [HttpGet]
    public ContentResult Get()
    {
        string jsonString = "{'Server': '.NET Application'}";
        return Content(jsonString, "application/json");
    }

    // GET /api/add/{num_1}/{num_2}
    [HttpGet("add/{number_1}/{number_2}")]
    public ContentResult Get(int number_1, int number_2)
    {
        int res = number_1 + number_2;
        string jsonString = $"{{'result': '{res}'}}";
        return Content(jsonString, "application/json");
    }

    // GET /api/str/{origin}/{target}/{replace}
    [HttpGet("str/{origin}/{target}/{replace}")]
    public ContentResult Get(string origin, string target, string replace)
    {
        string res = origin.Replace(target, replace);
        string jsonString = $"{{'result': '{res}'}}";
        return Content(jsonString, "application/json");
    }
}
