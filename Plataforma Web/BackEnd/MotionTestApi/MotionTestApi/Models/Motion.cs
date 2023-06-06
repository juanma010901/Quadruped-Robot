using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MotionTestApi.Models
{
    public class Motion
    {
        public int Id { get; set; }
        public bool Start { get; set; }
        public int TrackId { get; set; }
    }
}
